# DevTools cookie write/delete APIs allow extensions to modify cookies for enterprise policy-blocked sites despite runtime_blocked_hosts restrictions

| Field | Value |
|-------|-------|
| **Issue ID** | [479673903](https://issues.chromium.org/issues/479673903) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>DevTools |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | po...@gmail.com |
| **Assignee** | da...@google.com |
| **Created** | 2026-01-29 |
| **Bounty** | Confirmed (amount unknown) |

## Description

---

### Report description

DevTools cookie write/delete APIs allow extensions to modify cookies for enterprise policy-blocked sites despite runtime\_blocked\_hosts restrictions

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

Chromium enforces enterprise host restrictions for extensions via `runtime_blocked_hosts` in the `ExtensionSettings` policy. On Windows this can be configured, for example, as:

```
Windows Registry Editor Version 5.00

[HKEY_CURRENT_USER\Software\Policies\Google\Chrome\ExtensionSettings]
"*"="{\"runtime_blocked_hosts\":[\"https://www.google.com/*\"]}"

```

This is intended to ensure that extensions cannot interact with `https://www.google.com/*`, even if they have powerful permissions like `debugger`.

When an extension uses the `chrome.debugger` API, the DevTools client for extensions (`ExtensionDevToolsClientHost`) consults `ExtensionMayAttachToURL` / `ExtensionMayAttachToURLOrInnerURL`, which explicitly treats policy-blocked hosts as forbidden:

```
// chrome/browser/extensions/api/debugger/debugger_api.cc
bool ExtensionMayAttachToURL(const Extension& extension,
                             Profile* extension_profile,
                             const GURL& url,
                             std::string* error) {
  ...
  const GURL& url_for_restriction_check =
      url.SchemeIsBlob() ? url::Origin::Create(url).GetURL() : url;
  if (extension.permissions_data()->IsRestrictedUrl(url_for_restriction_check,
                                                    error)) {
    return false;
  }

  // Policy blocked hosts supersede the `debugger` permission.
  if (extension.permissions_data()->IsPolicyBlockedHost(url) ||
      extension.permissions_data()->IsPolicyBlockedHost(
          url_for_restriction_check)) {
    *error = kRestrictedError;
    return false;
  }
  ...
}

```

This correctly prevents an extension from attaching DevTools directly to a tab whose URL matches `runtime_blocked_hosts` (such as `https://www.google.com`).

However, once an extension is attached to any *allowed* tab, it can still use DevTools Protocol (CDP) commands that operate on the global cookie jar and supply arbitrary target URLs or domains. For cookie **read** operations, the implementation has been updated to use the DevTools client’s `MayAttachToURL` check when deciding which hosts are accessible:

```
// content/browser/devtools/protocol/network_handler.cc
void NetworkHandler::GetCookies(
    std::unique_ptr<Array<String>> protocol_urls,
    std::unique_ptr<GetCookiesCallback> callback) {
  ...
  std::vector<GURL> urls = ComputeCookieURLs(host_, protocol_urls);
  bool is_webui = host_ && host_->web_ui();

  std::erase_if(urls, [=, this](const GURL& url) {
    return !client_->MayAttachToURL(url, is_webui);
  });
  ...
}

```

and similarly for `GetAllCookies`, which filters the results using synthesized HTTP/HTTPS URLs per cookie domain. This ensures that enterprise host restrictions are applied to cookie **enumeration**.

In contrast, cookie **write/delete/clear** DevTools handlers do not perform any `MayAttachToURL` or policy-based checks on the target `url` or `domain`. They act only on the presence of a `StoragePartition` and the syntactic validity of the cookie parameters:

```
// content/browser/devtools/protocol/network_handler.cc
void NetworkHandler::SetCookie(
    const std::string& name,
    const std::string& value,
    std::optional<std::string> url,
    std::optional<std::string> domain,
    std::optional<std::string> path,
    std::optional<bool> secure,
    std::optional<bool> http_only,
    std::optional<std::string> same_site,
    std::optional<double> expires,
    std::optional<std::string> priority,
    std::optional<bool> same_party,
    std::optional<std::string> source_scheme,
    std::optional<int> source_port,
    std::unique_ptr<Network::CookiePartitionKey> partition_key,
    std::unique_ptr<SetCookieCallback> callback) {
  if (!storage_partition_) {
    callback->sendFailure(Response::InternalError());
    return;
  }

  auto cookie_or_error = MakeCookieFromProtocolValues(
      name, value, url.value_or(""), domain.value_or(""), path.value_or(""),
      secure.value_or(false), http_only.value_or(false), same_site.value_or(""),
      expires.value_or(-1), priority.value_or(""), source_scheme, source_port,
      partition_key);
  ...
  storage_partition_->GetCookieManagerForBrowserProcess()->SetCanonicalCookie(
      *cookie, net::cookie_util::SimulatedCookieSource(*cookie, "https"),
      options,
      base::BindOnce(net::cookie_util::IsCookieAccessResultInclude)
          .Then(base::BindOnce(&SetCookieCallback::sendSuccess,
                               std::move(callback))));
}

void NetworkHandler::DeleteCookies(
    const std::string& name,
    std::optional<std::string> url_spec,
    std::optional<std::string> domain,
    std::optional<std::string> path,
    std::unique_ptr<Network::CookiePartitionKey> partition_key,
    std::unique_ptr<DeleteCookiesCallback> callback) {
  if (!storage_partition_) {
    callback->sendFailure(Response::InternalError());
    return;
  }
  if (!url_spec.has_value() && !domain.has_value()) {
    callback->sendFailure(Response::InvalidParams(
        "At least one of the url and domain needs to be specified"));
  }
  ...
  cookie_manager->GetAllCookies(
      base::BindOnce(&DeleteFilteredCookies, base::Unretained(cookie_manager),
                     name, normalized_domain, path.value_or(""),
                     std::move(partition_key), std::move(callback)));
}

```

The storage domain DevTools handler exposes a similar cookie-clearing operation without policy checks:

```
// content/browser/devtools/protocol/storage_handler.cc
void StorageHandler::ClearCookies(
    std::optional<std::string> browser_context_id,
    std::unique_ptr<ClearCookiesCallback> callback) {
  StoragePartition* storage_partition = nullptr;
  Response response = StorageHandler::FindStoragePartition(browser_context_id,
                                                           &storage_partition);
  if (!response.IsSuccess()) {
    callback->sendFailure(std::move(response));
    return;
  }

  storage_partition->GetCookieManagerForBrowserProcess()->DeleteCookies(
      network::mojom::CookieDeletionFilter::New(),
      base::BindOnce([](std::unique_ptr<ClearCookiesCallback> callback,
                        uint32_t) { callback->sendSuccess(); },
                     std::move(callback)));
}

```

As a result, once an extension is attached to a tab that is *not* policy-blocked, it can use `chrome.debugger.sendCommand` to invoke:

- `Network.setCookie` with `url: "https://www.google.com/"`, to create or overwrite a cookie on a host that is policy-blocked for the extension.
- `Network.deleteCookies` with `domain: "www.google.com"`, to remove specific cookies for that host.
- `Storage.clearCookies`, to clear all cookies in the current profile’s cookie store, including those for policy-blocked sites such as `https://www.google.com/`.

The PoC extension in `web/devtools_cookies/extension` demonstrates this pattern. Its popup script attaches to the active tab and then calls DevTools cookie commands targeting `https://www.google.com/`:

```
// web/devtools_cookies/extension/popup.js
const PROTOCOL_VERSION = '1.3';
const TARGET_URL = 'https://www.google.com/';
const TARGET_DOMAIN = 'www.google.com';
...
function sendCommand(method, params) {
  ...
  chrome.debugger.sendCommand(debuggee, method, params, (result) => {
    ...
  });
}

document.getElementById('setCookie').addEventListener('click', () => {
  ensureAttached((ok) => {
    if (!ok) return;
    const params = {
      name: 'devtools_poc',
      value: 'ts_' + Date.now(),
      url: TARGET_URL,
      path: '/',
      secure: true,
      httpOnly: false
    };
    sendCommand('Network.setCookie', params);
  });
});

```

The extension only requires the `debugger` permission and user interaction to attach; it does not require host permissions for `https://www.google.com/`, and the enterprise `runtime_blocked_hosts` policy entry does not prevent these DevTools cookie operations.

Overall, this creates a discrepancy: cookie *reads* respect `runtime_blocked_hosts` via `MayAttachToURL`, while cookie *writes/deletes/clears* do not, allowing extensions to mutate cookie state on policy-blocked hosts.

#### 2. vulnerability reproduction

1. On Windows, import the provided policy file:
   - Double-click `web/devtools_cookies/policy_runtime_blocked_hosts_google.reg` to add the `ExtensionSettings` policy under `HKCU\Software\Policies\Google\Chrome`.
   - Restart Chrome and verify on `chrome://policy` that `ExtensionSettings` is present and `runtime_blocked_hosts` contains `https://www.google.com/*`.
2. In Chrome, open `chrome://extensions`, enable Developer mode, and load the unpacked extension from `web/devtools_cookies/extension`.
3. Open any tab that is **not** `https://www.google.com` (for example, `https://example.com`).
4. Click the extension’s toolbar icon:
   - Click “Attach to active tab” (step 1) to call `chrome.debugger.attach` for the current tab.
   - Click “Set poc cookie on [https://www.google.com/”](https://www.google.com/%E2%80%9D) (step 2). The extension invokes `Network.setCookie` with `url: "https://www.google.com/"`.
   - Optionally click “Delete poc cookie on [https://www.google.com/”](https://www.google.com/%E2%80%9D) (step 3) and “Clear all cookies in current profile” (step 4), which invoke `Network.deleteCookies` and `Storage.clearCookies`.
5. In a separate tab, visit `https://www.google.com` (or clear and then visit it) and observe that:
   - The `devtools_poc` cookie is present or has been removed according to the actions performed by the extension.
   - If you were logged in, removing or clearing cookies can force sign-out and disrupt the session.

These steps show that an extension subject to `runtime_blocked_hosts: ["https://www.google.com/*"]` can still modify (`set`, `delete`, or clear) cookies for `https://www.google.com/` via DevTools cookie APIs, even though direct attachment to that URL is correctly blocked.

#### Impact analysis

- **Who can exploit it:** Any installed extension that declares the `debugger` permission and can run in an environment where administrators configure `runtime_blocked_hosts` to restrict host access (for example, adding `https://www.google.com/*`). A user must interact with the extension (e.g., click its action) to allow it to attach to some non-policy-blocked tab via `chrome.debugger.attach`.
- **What they gain:** Once attached to an allowed tab, the extension can use DevTools cookie APIs (`Network.setCookie`, `Network.deleteCookies`, `Storage.clearCookies`) to modify cookies for hosts that are policy-blocked for that extension, including `https://www.google.com/`. Practically, this enables:
  
  - Injecting or overwriting cookies on policy-blocked sites (which may influence site behavior or application state, and could become more serious in combination with site-side weaknesses such as session fixation vulnerabilities).
  - Deleting specific cookies or clearing all cookies, forcing sign-outs and disrupting user sessions on policy-blocked sites.
- **Security significance (classification):** This is best categorized as a **Permissions Bypass** / enterprise policy enforcement bypass for extension host restrictions. It does not grant the ability to read cookie values that are otherwise protected, nor does it provide remote code execution, a sandbox escape, or a privilege escalation beyond the extension’s existing capabilities. However, it weakens administrator expectations that `runtime_blocked_hosts` completely prevents extensions from influencing sensitive sites, by allowing extensions to tamper with cookie-based session and configuration state on those policy-blocked hosts.

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

- [devtools_cookies.mp4](attachments/devtools_cookies.mp4) (video/mp4, 4.7 MB)
- [devtools_cookies.zip](attachments/devtools_cookies.zip) (application/x-zip-compressed, 2.7 KB)

## Timeline

### po...@gmail.com (2026-01-29)

#### patch

```
diff --git a/content/browser/devtools/protocol/network_handler.h b/content/browser/devtools/protocol/network_handler.h
index 1111111111..2222222222 100644
--- a/content/browser/devtools/protocol/network_handler.h
+++ b/content/browser/devtools/protocol/network_handler.h
@@ -111,9 +111,11 @@ class NetworkHandler : public DevToolsDomainHandler,
       const std::string& resource_type,
       base::flat_set<blink::mojom::ResourceType>* intercepted_resource_types);
   static std::unique_ptr<Array<Network::Cookie>> BuildCookieArray(
       const std::vector<net::CanonicalCookie>& cookie_list);
   static void SetCookies(
       StoragePartition* storage_partition,
+      DevToolsAgentHostClient* client,
+      bool is_webui,
       std::unique_ptr<protocol::Array<Network::CookieParam>> cookies,
       base::OnceCallback<void(bool)> callback);

   void Wire(UberDispatcher* dispatcher) override;
   void SetRenderer(int render_process_id,
@@ -196,7 +198,8 @@ class NetworkHandler : public DevToolsDomainHandler,
                  std::optional<int> source_port,
                  std::unique_ptr<Network::CookiePartitionKey> partition_key,
                  std::unique_ptr<SetCookieCallback> callback) override;
   void SetCookies(
       std::unique_ptr<protocol::Array<Network::CookieParam>> cookies,
       std::unique_ptr<SetCookiesCallback> callback) override;

diff --git a/content/browser/devtools/protocol/network_handler.cc b/content/browser/devtools/protocol/network_handler.cc
index 1111111111..2222222222 100644
--- a/content/browser/devtools/protocol/network_handler.cc
+++ b/content/browser/devtools/protocol/network_handler.cc
@@ -230,6 +230,21 @@ void NetworkHandler::GotAllCookies(
   callback->sendSuccess(NetworkHandler::BuildCookieArray(filtered_cookies));
 }

 void NetworkHandler::SetCookie(
     const std::string& name,
@@ -254,6 +269,24 @@ void NetworkHandler::SetCookie(
   }
   std::unique_ptr<net::CanonicalCookie> cookie =
       std::get<std::unique_ptr<net::CanonicalCookie>>(
           std::move(cookie_or_error));

+  // Enforce client policy for the cookie's effective domain.
+  if (client_) {
+    const std::string domain_without_dot = cookie->DomainWithoutDot();
+    if (!domain_without_dot.empty()) {
+      const bool is_webui = host_ && host_->web_ui();
+      GURL https_url(
+          base::StrCat({url::kHttpsScheme, url::kStandardSchemeSeparator,
+                        domain_without_dot}));
+      GURL http_url(
+          base::StrCat({url::kHttpScheme, url::kStandardSchemeSeparator,
+                        domain_without_dot}));
+      if (!client_->MayAttachToURL(https_url, is_webui) ||
+          !client_->MayAttachToURL(http_url, is_webui)) {
+        callback->sendSuccess();
+        return;
+      }
+    }
+  }
+
   net::CookieOptions options;
   // Permit it to set a SameSite cookie if it wants to.
   options.set_same_site_cookie_context(
       net::CookieOptions::SameSiteCookieContext::MakeInclusive());
   options.set_include_httponly();
@@ -262,12 +295,14 @@ void NetworkHandler::SetCookie(
       base::BindOnce(net::cookie_util::IsCookieAccessResultInclude)
           .Then(base::BindOnce(&SetCookieCallback::sendSuccess,
                                std::move(callback))));
 }

 // static
 void NetworkHandler::SetCookies(
     StoragePartition* storage_partition,
+    DevToolsAgentHostClient* client,
+    bool is_webui,
     std::unique_ptr<protocol::Array<Network::CookieParam>> cookies,
     base::OnceCallback<void(bool)> callback) {
   std::vector<std::unique_ptr<net::CanonicalCookie>> net_cookies;
   for (const std::unique_ptr<Network::CookieParam>& cookie : *cookies) {
@@ -291,13 +326,33 @@ void NetworkHandler::SetCookies(
         cookie->GetDomain(""), cookie->GetPath(""), cookie->GetSecure(false),
         cookie->GetHttpOnly(false), cookie->GetSameSite(""),
         cookie->GetExpires(-1), cookie->GetPriority(""), source_scheme,
         source_port, partition_key);
     if (std::holds_alternative<Response>(net_cookie_or_error)) {
       // TODO: Investiage whether we can report the error as a protocol error
       // (this might be a breaking CDP change).
       std::move(callback).Run(false);
       return;
     }
-    net_cookies.push_back(std::get<std::unique_ptr<net::CanonicalCookie>>(
-        std::move(net_cookie_or_error)));
+    std::unique_ptr<net::CanonicalCookie> net_cookie =
+        std::get<std::unique_ptr<net::CanonicalCookie>>(
+            std::move(net_cookie_or_error));
+
+    // Enforce client policy for the cookie's effective domain when a client is
+    // present (for example, extension DevTools clients that honor
+    // runtime_blocked_hosts).
+    if (client) {
+      const std::string domain_without_dot = net_cookie->DomainWithoutDot();
+      if (!domain_without_dot.empty()) {
+        GURL https_url(
+            base::StrCat({url::kHttpsScheme, url::kStandardSchemeSeparator,
+                          domain_without_dot}));
+        GURL http_url(
+            base::StrCat({url::kHttpScheme, url::kStandardSchemeSeparator,
+                          domain_without_dot}));
+        if (!client->MayAttachToURL(https_url, is_webui) ||
+            !client->MayAttachToURL(http_url, is_webui)) {
+          continue;
+        }
+      }
+    }
+
+    net_cookies.push_back(std::move(net_cookie));
   }

   base::RepeatingClosure barrier_closure = base::BarrierClosure(
       net_cookies.size(), base::BindOnce(std::move(callback), true));
@@ -311,11 +366,13 @@ void NetworkHandler::SetCookies(
         base::BindOnce([](base::RepeatingClosure callback,
                           net::CookieAccessResult) { callback.Run(); },
                        barrier_closure));
   }
 }

 void NetworkHandler::SetCookies(
     std::unique_ptr<protocol::Array<Network::CookieParam>> cookies,
     std::unique_ptr<SetCookiesCallback> callback) {
   if (!storage_partition_) {
@@ -324,7 +381,9 @@ void NetworkHandler::SetCookies(
   }

   NetworkHandler::SetCookies(
-      storage_partition_, std::move(cookies),
+      storage_partition_, client_, host_ && host_->web_ui(),
+      std::move(cookies),
       base::BindOnce(
           [](std::unique_ptr<SetCookiesCallback> callback, bool success) {
             if (success) {
@@ -332,6 +391,8 @@ void NetworkHandler::SetCookies(
             } else {
               callback->sendFailure(
                   Response::InvalidParams(kInvalidCookieFields));
             }
           },
           std::move(callback)));
 }

 void NetworkHandler::DeleteCookies(
@@ -345,6 +406,8 @@ void NetworkHandler::DeleteCookies(
   if (!storage_partition_) {
     callback->sendFailure(Response::InternalError());
     return;
   }
@@ -355,6 +418,25 @@ void NetworkHandler::DeleteCookies(
   }

   std::string normalized_domain = domain.value_or("");
   if (normalized_domain.empty()) {
@@ -364,9 +446,28 @@ void NetworkHandler::DeleteCookies(
       callback->sendFailure(Response::InvalidParams(
           "An http or https url URL must be specified"));
       return;
     }
     normalized_domain = url.GetHost();
   }

+  // Enforce client policy for the target host. For clients such as extensions
+  // that restrict attachment via MayAttachToURL, silently ignore delete
+  // requests for disallowed hosts.
+  if (client_) {
+    const bool is_webui = host_ && host_->web_ui();
+    if (!normalized_domain.empty()) {
+      GURL https_url(base::StrCat(
+          {url::kHttpsScheme, url::kStandardSchemeSeparator,
+           normalized_domain}));
+      GURL http_url(base::StrCat(
+          {url::kHttpScheme, url::kStandardSchemeSeparator,
+           normalized_domain}));
+      if (!client_->MayAttachToURL(https_url, is_webui) ||
+          !client_->MayAttachToURL(http_url, is_webui)) {
+        callback->sendSuccess();
+        return;
+      }
+    }
+  }
+
   auto* cookie_manager =
       storage_partition_->GetCookieManagerForBrowserProcess();

   cookie_manager->GetAllCookies(
@@ -216,11 +297,21 @@ void NetworkHandler::ClearBrowserCache(
       content::BrowsingDataRemover::ORIGIN_TYPE_UNPROTECTED_WEB,
       new DevtoolsClearCacheObserver(remover, std::move(callback)));
 }

 void NetworkHandler::ClearBrowserCookies(
     std::unique_ptr<ClearBrowserCookiesCallback> callback) {
   if (!storage_partition_) {
     callback->sendFailure(Response::InternalError());
     return;
   }

+  // Clearing all cookies in a profile is a powerful operation. Disallow it for
+  // untrusted clients such as extension DevTools, while still allowing it for
+  // trusted DevTools frontends and other internal callers.
+  if (client_ && !client_->IsTrusted()) {
+    callback->sendFailure(Response::ServerError(
+        "Clearing all browser cookies is not allowed for this client"));
+    return;
+  }
+
   storage_partition_->GetCookieManagerForBrowserProcess()->DeleteCookies(
       network::mojom::CookieDeletionFilter::New(),
       base::BindOnce([](std::unique_ptr<ClearBrowserCookiesCallback> callback,
                         uint32_t) { callback->sendSuccess(); },
diff --git a/content/browser/devtools/protocol/storage_handler.cc b/content/browser/devtools/protocol/storage_handler.cc
index 1111111111..2222222222 100644
--- a/content/browser/devtools/protocol/storage_handler.cc
+++ b/content/browser/devtools/protocol/storage_handler.cc
@@ -504,13 +504,18 @@ void StorageHandler::SetCookies(
   Response response = StorageHandler::FindStoragePartition(browser_context_id,
                                                            &storage_partition);
   if (!response.IsSuccess()) {
     callback->sendFailure(std::move(response));
     return;
   }

+  bool is_webui = frame_host_ && frame_host_->web_ui();
+
   NetworkHandler::SetCookies(
-      storage_partition, std::move(cookies),
+      storage_partition, client_, is_webui, std::move(cookies),
       base::BindOnce(
           [](std::unique_ptr<SetCookiesCallback> callback, bool success) {
             if (success) {
               callback->sendSuccess();
             } else {
               callback->sendFailure(
@@ -520,13 +525,25 @@ void StorageHandler::SetCookies(
 }

 void StorageHandler::ClearCookies(
     std::optional<std::string> browser_context_id,
     std::unique_ptr<ClearCookiesCallback> callback) {
   StoragePartition* storage_partition = nullptr;
   Response response = StorageHandler::FindStoragePartition(browser_context_id,
                                                            &storage_partition);
   if (!response.IsSuccess()) {
     callback->sendFailure(std::move(response));
     return;
   }

+  // Clearing all cookies in a profile is a powerful operation. Disallow it for
+  // untrusted clients such as extension DevTools, while still allowing it for
+  // trusted DevTools frontends and other internal callers.
+  if (client_ && !client_->IsTrusted()) {
+    callback->sendFailure(Response::ServerError(
+        "Clearing all browser cookies is not allowed for this client"));
+    return;
+  }
+
   storage_partition->GetCookieManagerForBrowserProcess()->DeleteCookies(
       network::mojom::CookieDeletionFilter::New(),
       base::BindOnce([](std::unique_ptr<ClearCookiesCallback> callback,
                         uint32_t) { callback->sendSuccess(); },
                      std::move(callback)));


```

### el...@chromium.org (2026-01-29)

Security shepherd: thanks for the report! I have not run your PoC (the setup seems a little involved) but I have confirmed via code inspection that this bug is present. Over to the devtools team. I think this is going to be Sev-3 from us, since it requires the attacker to already have a very powerful permission (a live, attached debugger extension) and only allows *writing* cookies, not reading them.

### el...@chromium.org (2026-01-29)

Setting OS based on where this policy is present and FoundIn based on the original report.

### ya...@google.com (2026-02-10)

Danil, could you take a look at this in M147? This seems like an oversight.

### dx...@google.com (2026-02-26)

Project: chromium/src  

Branch:  main  

Author:  Danil Somsikov [dsv@chromium.org](mailto:dsv@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7597631>

Refactor DevTools cookie handling for better access control.

---


Expand for full commit details
```
     
    This change introduces a static `NetworkHandler::CanAccessCookie` method to centralize permission checks for accessing cookies. The `NetworkHandler::ClearCookies` static method is added to provide a unified way to clear cookies, used by both `Network.clearBrowserCookies` and `Storage.clearCookies`. The `SetCookies` methods are updated to use the new permission check. The `FilterCookies` helper is made more flexible by using optional parameters and a flag for partition key filtering. 
     
    Bug: 479673903 
    Change-Id: Idcff402bff288c58771d42b75f143b83557279e7 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7597631 
    Commit-Queue: Danil Somsikov <dsv@chromium.org> 
    Auto-Submit: Danil Somsikov <dsv@chromium.org> 
    Reviewed-by: Andrey Kosyakov <caseq@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1590697}

```

---

Files:

- M `content/browser/devtools/protocol/devtools_protocol_browsertest.cc`
- M `content/browser/devtools/protocol/network_handler.cc`
- M `content/browser/devtools/protocol/network_handler.h`
- M `content/browser/devtools/protocol/storage_handler.cc`
- M `third_party/blink/web_tests/http/tests/inspector-protocol/storage/cookies-expected.txt`

---

Hash: [9a6fcf26c50b7aa77f158bb1a807b0d0137ce624](https://chromiumdash.appspot.com/commit/9a6fcf26c50b7aa77f158bb1a807b0d0137ce624)  

Date: Thu Feb 26 08:52:26 2026


---

### sh...@microsoft.com (2026-03-08)

**Subject: Behavioral regression in Network.clearBrowserCookies**

Hi danilsomsikov@, caseq@,

We noticed a behavioral regression introduced by this CL in `Network.clearBrowserCookies`.

**Before this change**, `ClearBrowserCookies` used a single atomic `CookieManager::DeleteCookies(empty_filter)` mojo call, which meant the deletion was effectively complete by the time the CDP response was sent.

**After this change**, `ClearBrowserCookies` now delegates to `NetworkHandler::ClearCookies`, which does a two-step process: `GetAllCookies()` → `DeleteCanonicalCookie()` for each cookie individually. This creates a race condition for CDP clients that issue `Network.clearBrowserCookies` followed by `Network.getAllCookies` (or `Network.getCookies`) — the second command can be dispatched and complete before the deletion loop finishes, returning cookies that haven't been deleted yet.

This broke our WebView2 test (`EmbeddedBrowserCookieTest.CreateAddDelete`) which does:

1. Add cookies via `Network.setCookie`
2. `Network.clearBrowserCookies` (fire-and-forget)
3. `Network.getAllCookies` → expects 0 cookies ← **fails because cookies not yet deleted**

We understand the motivation for centralizing access control checks via `CanAccessCookie`. However, we'd like to ask: **could the access-control-aware deletion still use an atomic `DeleteCookies` approach** rather than the get-then-delete-each pattern? For example:

```
void NetworkHandler::ClearCookies(StoragePartition* storage_partition,
                                  DevToolsAgentHostClient& client,
                                  bool is_webui,
                                  base::OnceClosure callback) {
  // For trusted clients that can access all cookies, use the atomic path
  // to preserve the original behavior and avoid race conditions.
  storage_partition->GetCookieManagerForBrowserProcess()->DeleteCookies(
      network::mojom::CookieDeletionFilter::New(),
      base::BindOnce([](base::OnceClosure cb, uint32_t) { std::move(cb).Run(); },
                     std::move(callback)));
}

```

Or alternatively, if per-cookie access checking is required for `ClearCookies`, the access check could be applied as a filter on `CookieDeletionFilter` rather than fetching all cookies first.

This would preserve the atomic semantics that CDP clients depend on, while still supporting the access control requirements.

Thanks for considering this!

### dx...@google.com (2026-03-18)

Project: chromium/src  

Branch:  main  

Author:  Xiaochen [xiaocw@microsoft.com](mailto:xiaocw@microsoft.com)  

Link:    <https://chromium-review.googlesource.com/7656906>

devtools: Restore atomic cookie deletion for trusted CDP clients

---


Expand for full commit details
```
     
    CL 7597631 fixed a security issue where extensions could modify cookies 
    beyond their permission scope via CDP cookie APIs. However, the fix 
    changed all CDP clients to use a per-cookie filtering path for 
    clearBrowserCookies, causing performance regression and loss of 
    atomicity for trusted clients (DevTools, Playwright, WebView2). 
     
    Add DevToolsAgentHostClient::MayAccessAllCookies() to express whether a 
    client has unrestricted cookie access. Keep the default conservative 
    (false), override it to true for trusted built-in clients, and return 
    false for extension debugger clients. In NetworkHandler::ClearCookies, 
    trusted clients use the original atomic DeleteCookies(empty_filter) 
    path, while extension clients continue using the filtered per-cookie 
    deletion path. 
     
    Bug: 479673903 
    Change-Id: I1ad699dd7d246c7742d03458fe6f963fef58883b 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7656906 
    Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org> 
    Reviewed-by: Andrey Kosyakov <caseq@chromium.org> 
    Commit-Queue: Xiaochen Wu <xiaocw@microsoft.com> 
    Cr-Commit-Position: refs/heads/main@{#1600901}

```

---

Files:

- M `chrome/browser/devtools/devtools_ui_bindings.cc`
- M `chrome/browser/devtools/devtools_ui_bindings.h`
- M `chrome/browser/devtools/views/devtools_floaty.cc`
- M `chrome/browser/extensions/api/debugger/debugger_api.cc`
- M `components/devtools/simple_devtools_protocol_client/simple_devtools_protocol_client.cc`
- M `components/devtools/simple_devtools_protocol_client/simple_devtools_protocol_client.h`
- M `content/browser/devtools/devtools_http_handler.cc`
- M `content/browser/devtools/devtools_pipe_handler.cc`
- M `content/browser/devtools/devtools_pipe_handler.h`
- M `content/browser/devtools/protocol/devtools_protocol_browsertest.cc`
- M `content/browser/devtools/protocol/network_handler.cc`
- M `content/browser/devtools/protocol/target_handler.cc`
- M `content/public/browser/devtools_agent_host_client.cc`
- M `content/public/browser/devtools_agent_host_client.h`
- M `content/public/test/test_devtools_protocol_client.cc`
- M `content/public/test/test_devtools_protocol_client.h`
- M `content/shell/browser/shell_devtools_bindings.cc`
- M `content/shell/browser/shell_devtools_bindings.h`

---

Hash: [8c3121e4ee4128f81844b069f86254f45bf1c5f0](https://chromiumdash.appspot.com/commit/8c3121e4ee4128f81844b069f86254f45bf1c5f0)  

Date: Wed Mar 18 00:19:40 2026


---

### sp...@google.com (2026-05-26)

*NOTE: This is an automatically generated email*

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this
issue does not meet the criteria to qualify for a reward.

Rationale for this decision:

Not web exploitable

Note that the fact that this issue is not being rewarded does not mean
that the product team won't fix the issue. We have filed a bug with the product
team and they will review your report and decide if a fix is required. We'll
let you know if the issue was fixed.

Regards,   

Google Security Bot

*How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

### ch...@google.com (2026-06-05)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Not web exploitable
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
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/479673903)*
