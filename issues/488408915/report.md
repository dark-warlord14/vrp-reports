# SharedStorage custom-data-origin authorization bypass via stale match state

| Field | Value |
|-------|-------|
| **Issue ID** | [488408915](https://issues.chromium.org/issues/488408915) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Storage>SharedStorage |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | oj...@gmail.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2026-02-27 |
| **Bounty** | $1,000.00 |

## Description

---

### Report description

SharedStorage custom-data-origin authorization bypass via stale match state

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://github.com/chromium/chromium>

---

### The problem

#### Please describe the technical details of the vulnerability

## Executive summary

`SharedStorageWorkletHost::OnJsonParsed()` in `content/browser/shared_storage/shared_storage_worklet_host.cc` keeps `script_origin_match` and `context_origin_match` state across loop iterations when evaluating `/.well-known/shared-storage/trusted-origins`.

Because the two booleans are declared outside the loop and never reset per entry, a `scriptOrigin` match from one JSON entry can be combined with a `contextOrigin` match from another entry. This breaks the intended per-entry pair authorization model for custom `dataOrigin` in `sharedStorage.createWorklet()`.

Result: unauthorized worklet creation can succeed for `(scriptOrigin, contextOrigin)` pairs that are never authorized together in a single trusted-origins entry.

## Affected builds and status

- Reproduced on Chromium ASAN build: `147.0.7703.0` (`chrome-asan/content_shell`).
- Local source snapshot inspected: Chromium `147.0.7686.0` codebase; vulnerable logic is present.
- Feature gate status:
  - `blink::features::kSharedStorageCreateWorkletCustomDataOrigin` is `FEATURE_ENABLED_BY_DEFAULT`.
  - `network::features::kSharedStorageAPI` is `FEATURE_ENABLED_BY_DEFAULT`.

## Root cause

In `OnJsonParsed()`, these variables are initialized once and reused:

```
bool script_origin_match = false;
bool context_origin_match = false;
for (const base::Value& item_value : result.value()) {
  ...
  if (!script_origin_match) {
    continue;
  }
  ...
  if (script_origin_match && context_origin_match) {
    SetDataOriginOptInResultAndMaybeFinish(/*opted_in=*/true, ...);
    return;
  }
}

```

If entry `N` sets `script_origin_match = true`, entry `N+1` may set `context_origin_match = true` and immediately pass the final check, even when no single entry authorizes the pair.

### Preconditions / exploitability constraints

- Victim data origin must host a multi-entry `/.well-known/shared-storage/trusted-origins`.
- Entries must allow split-match condition:
  - one entry matches attacker-controlled/chosen script origin
  - another entry matches attacker context origin
  - no single entry authorizes both together
- Attacker must be able to load a compatible cross-origin worklet script URL (CORS-permitted).
- This bug affects custom `dataOrigin` authorization path (`needs_data_origin_opt_in_`).

## Reproduction

PoC: `reproduce.py`

### Requirements

- Linux
- Python 3
- `openssl`
- Chromium `content_shell`

### Run

```
python3 reproduce.py /path/to/chrome-asan/content_shell

```
### Observed result

PoC reproduced successfully in this environment:

- `GET /.well-known/shared-storage/trusted-origins` requested from `c.test`
- `GET /worklet.js` requested from `b.test`
- Console output includes:
  - `BUG_CONFIRMED: createWorklet succeeded without authorization`

## Proposed fix

Reset match state per JSON item:

```
for (const base::Value& item_value : result.value()) {
  bool script_origin_match = false;
  bool context_origin_match = false;
  ...
}

```

Any equivalent refactor that guarantees per-item independent evaluation is acceptable.

#### Impact analysis

## Exploit scenario

Data origin (`c.test`) publishes:

```
[
  {"scriptOrigin": "https://b.test", "contextOrigin": "https://d.test"},
  {"scriptOrigin": "https://d.test", "contextOrigin": "https://a.test"}
]

```

Attacker page on `a.test` executes:

```
await sharedStorage.createWorklet(
  "https://b.test/worklet.js",
  { dataOrigin: "https://c.test" }
);

```

No single entry authorizes `(scriptOrigin=b.test, contextOrigin=a.test)`, but current logic accepts due to cross-entry state carry-over.

## Impact

### Security impact

When bypass succeeds, attacker-created worklet runs with `shared_storage_origin_ = dataOrigin` and can operate on that origin's Shared Storage namespace (subject to regular API/runtime permissions checks).

This can enable unauthorized reads/writes that were meant to require explicit pair authorization by the data-origin owner.

---

### The cause

#### What version of Chrome have you found the security issue in?

147.0.7703.0

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Auth Bypass

#### How would you like to be publicly acknowledged for your report?

M. Fauzan Wijaya (Gh05t666nero)

## Attachments

- [reproduce.py](attachments/reproduce.py) (text/x-python, 6.7 KB)
- [poc.html](attachments/poc.html) (text/html, 1.3 KB)
- [server.py](attachments/server.py) (text/x-python, 4.6 KB)
- [trusted-origins.json](attachments/trusted-origins.json) (application/json, 169 B)
- [worklet.js](attachments/worklet.js) (text/javascript, 150 B)
- [poc.html](attachments/poc_73958830.html) (text/html, 1.7 KB)
- [seed.html](attachments/seed.html) (text/html, 644 B)
- [server.py](attachments/server_73950946.py) (text/x-python, 4.2 KB)
- [trusted-origins.json](attachments/trusted-origins_73950947.json) (application/json, 169 B)
- [verify.html](attachments/verify.html) (text/html, 908 B)
- [verify-worklet.js](attachments/verify-worklet.js) (text/javascript, 337 B)
- [worklet.js](attachments/worklet_73960935.js) (text/javascript, 601 B)

## Timeline

### aj...@google.com (2026-02-27)

Hello this isn't easy for us to reproduce - could you separate out the reproduction steps:

1. Chrome command line with all necessary flags e.g. `chrome --enable-features=FeatureName http://localhost:8001`
2. distinct html poc files attached to this report as files `poc.html`
3. python server that manipulates headers and doesn't do anything else

Mixing running chrome and serving the files means this is more complex than necessary. Please do this and we will take a look.

### oj...@gmail.com (2026-02-27)

Thank you for the feedback. Here are the separated reproduction steps as requested.

## Files attached

| File | Description |
| --- | --- |
| `poc.html` | Attacker page that calls `sharedStorage.createWorklet()` with an unauthorized `(scriptOrigin, contextOrigin)` pair |
| `worklet.js` | Minimal SharedStorage worklet module (served from script origin) |
| `trusted-origins.json` | The `/.well-known/shared-storage/trusted-origins` payload served by the data origin. Contains two entries where **no single entry** authorizes `(scriptOrigin=b.test, contextOrigin=a.test)` together |
| `server.py` | Minimal Python 3 HTTPS server — only routes requests to the static files above with appropriate headers (CORS, `Shared-Storage-Cross-Origin-Worklet-Allowed`) |

## Step 1: Start the server

```
python3 server.py

```

This starts three HTTPS origins on localhost:

- `a.test:8443` — attacker context (serves `poc.html`)
- `b.test:8444` — script origin (serves `worklet.js` with CORS + `Shared-Storage-Cross-Origin-Worklet-Allowed: ?1`)
- `c.test:8445` — data origin (serves `trusted-origins.json` at `/.well-known/shared-storage/trusted-origins` with CORS)

A self-signed certificate covering all test domains is auto-generated on first run (requires `openssl`).

## Step 2: Launch Chrome

```
google-chrome \
  --host-resolver-rules="MAP a.test 127.0.0.1,MAP b.test 127.0.0.1,MAP c.test 127.0.0.1,MAP d.test 127.0.0.1" \
  --ignore-certificate-errors \
  --enable-features=PrivacySandboxAdsAPIsOverride,OverridePrivacySandboxSettingsLocalTesting,SharedStorageAPI,SharedStorageCreateWorkletCustomDataOrigin,FencedFrames,PrivateAggregationApi \
  --disable-features=EnforcePrivacySandboxAttestations \
  --no-sandbox \
  --user-data-dir=/tmp/ss-poc-profile \
  https://a.test:8443/poc.html

```

Tested and confirmed on **Google Chrome 145.0.7632.75** (Linux).

For `Chrome ASAN Build / Chromium Shell (content_shell)` (fewer flags needed, no attestation/pref gates):

```
./chrome-asan/content_shell \
  --host-resolver-rules="MAP a.test 127.0.0.1,MAP b.test 127.0.0.1,MAP c.test 127.0.0.1,MAP d.test 127.0.0.1" \
  --ignore-certificate-errors \
  --enable-features=PrivacySandboxAdsAPIsOverride,SharedStorageAPI,SharedStorageCreateWorkletCustomDataOrigin \
  --no-sandbox \
  --user-data-dir=/tmp/ss-poc-profile \
  https://a.test:8443/poc.html

```
### Flag explanation

| Flag | Purpose |
| --- | --- |
| `--host-resolver-rules=MAP ...` | Route `.test` domains to `127.0.0.1` |
| `--ignore-certificate-errors` | Accept the self-signed certificate |
| `--enable-features=SharedStorageAPI` | Enable SharedStorage API |
| `--enable-features=SharedStorageCreateWorkletCustomDataOrigin` | Enable custom `dataOrigin` in `createWorklet()` |
| `--enable-features=PrivacySandboxAdsAPIsOverride` | Override Privacy Sandbox API gates |
| `--enable-features=OverridePrivacySandboxSettingsLocalTesting` | Bypass Privacy Sandbox user preference checks (Chrome only) |
| `--enable-features=FencedFrames,PrivateAggregationApi` | Enable dependent APIs so `addModule()` is permitted |
| `--disable-features=EnforcePrivacySandboxAttestations` | Skip origin attestation check for `.test` domains (Chrome only) |
| `--no-sandbox` | Required for some Linux environments |
| `--user-data-dir=/tmp/ss-poc-profile` | Use a clean profile |

## Step 3: Observe result

The page will display one of:

- **`BUG_CONFIRMED: createWorklet succeeded without authorization`** — the bug is present. The `(scriptOrigin=b.test:8444, contextOrigin=a.test:8443)` pair was accepted despite no single entry in `trusted-origins.json` authorizing this pair together.
- **`DENIED: ...`** — the bug has been fixed or the feature is not active.

## What the trusted-origins.json contains

```
[
  {"scriptOrigin": "https://b.test:8444", "contextOrigin": "https://d.test:9999"},
  {"scriptOrigin": "https://d.test:9999", "contextOrigin": "https://a.test:8443"}
]

```

- Entry 0 authorizes `scriptOrigin=b.test` paired with `contextOrigin=d.test` (not `a.test`)
- Entry 1 authorizes `scriptOrigin=d.test` paired with `contextOrigin=a.test` (not `b.test`)

The PoC calls `createWorklet("https://b.test:8444/worklet.js", {dataOrigin: "https://c.test:8445"})` from page context `a.test:8443`.

No single entry authorizes `(scriptOrigin=b.test:8444, contextOrigin=a.test:8443)`. The bug causes `script_origin_match` from entry 0 to carry over into entry 1's evaluation, where `context_origin_match` becomes true, incorrectly passing the authorization check.

## Header summary

The Python server adds these headers (and nothing else beyond standard HTTP):

| Origin | Path | Special headers |
| --- | --- | --- |
| b.test:8444 | `/worklet.js` | `Access-Control-Allow-Origin: *`, `Shared-Storage-Cross-Origin-Worklet-Allowed: ?1` |
| c.test:8445 | `/.well-known/shared-storage/trusted-origins` | `Access-Control-Allow-Origin: *` |
| a.test:8443 | `/poc.html` | (none) |

### pe...@google.com (2026-02-27)

Thank you for providing more feedback. Adding the requester to the CC list.

### mp...@google.com (2026-03-04)

I don't think this is a bug but cammie@ probably knows.

### mp...@google.com (2026-03-04)

Reporter, your PoC doesn't clearly show any harm to users in Chrome it just prints that it has succeeded. Can you show any user harm that would come of this?

### oj...@gmail.com (2026-03-04)

Regarding #5 and #6, this is a spec-deviating authorization bypass with concrete user harm.

This bug is real and deviates from spec

The WICG spec (<https://wicg.github.io/shared-storage/>) defines the trusted-origins validation loop as:

For each item of parsed:
Let doesMatch be the result of running check for script and context origin match(...)
If doesMatch is true: break

doesMatch is a per-entry variable, computed fresh each iteration. The Chromium implementation at shared\_storage\_worklet\_host.cc instead declares two booleans (script\_origin\_match, context\_origin\_match) outside the loop and never resets them. This lets a scriptOrigin match from entry N carry over into entry N+1, where a contextOrigin match from a different entry completes the check. No single entry needs to authorize the pair.

User harm

I've updated the PoC to show concrete harm beyond "createWorklet succeeded". The updated files are attached.

After the unauthorized worklet is created, it runs with shared\_storage\_origin\_ = c.test (the victim's data partition). The worklet can then:

1. Read victim data: the steal-data operation calls sharedStorage.get("user\_segment") and returns a URL index encoding the value. The selected URL is loaded in a fenced frame, and the server logs which URL was fetched (proving data was read). If c.test stored user\_segment=premium\_user, the server sees /exfil?v=STOLEN\_premium\_user.
2. Tamper victim data: the tamper-data operation overwrites user\_segment to HIJACKED\_BY\_ATTACKER, injects an attacker\_flag key, and deletes experiment\_id and account\_tier. Visiting verify.html on c.test confirms the data was modified.

Updated reproduction steps

python3 server.py

Then launch Chrome:

google-chrome   

--host-resolver-rules="MAP a.test 127.0.0.1,MAP b.test 127.0.0.1,MAP c.test 127.0.0.1,MAP d.test 127.0.0.1"   

--ignore-certificate-errors   

--enable-features=PrivacySandboxAdsAPIsOverride,OverridePrivacySandboxSettingsLocalTesting,SharedStorageAPI,SharedStorageCreateWorkletCustomDataOrigin,FencedFrames   

--disable-features=EnforcePrivacySandboxAttestations   

--no-sandbox --user-data-dir=/tmp/ss-poc-profile   

<https://c.test:8445/seed.html>

1. Visit <https://c.test:8445/seed.html> to seed victim data (user\_segment, experiment\_id, account\_tier)
2. Visit <https://a.test:8443/poc.html> to run the exploit. Console and page show:
   - BUG\_CONFIRMED: createWorklet succeeded (unauthorized pair accepted)
   - selectURL completes, fenced frame loads exfiltrated result
   - tamper done: user\_segment overwritten, experiment\_id deleted
3. Server terminal prints "EXFIL HIT: STOLEN\_premium\_user"
4. Visit <https://c.test:8445/verify.html>, fenced frame shows TAMPERED\_CONFIRMED

Files attached

server.py HTTPS server for all three origins
seed.html Pre-seeds victim data in c.test's Shared Storage
poc.html Attacker page: bypass, exfiltrate, tamper
worklet.js Worklet with steal-data and tamper-data operations
verify.html Legitimate c.test page to confirm tampering
verify-worklet.js Same-origin worklet to read back tampered data
trusted-origins.json Two entries with split-match condition (unchanged)

The attacker on a.test gains full read/write/delete access to c.test's Shared Storage partition without c.test ever authorizing the (scriptOrigin=b.test, contextOrigin=a.test) pair together. This breaks the per-entry authorization model that trusted-origins is designed to enforce.

### pe...@google.com (2026-03-04)

Thank you for providing more feedback. Adding the requester to the CC list.

### ch...@google.com (2026-03-11)

Setting Priority to P3 to match Severity s3. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### ca...@chromium.org (2026-03-13)

I think that this is true bug. I wrote this code, and it seems that I forgot to reset state at the end of each loop iteration. Thank you for catching this! I will write a patch to fix it.

### dx...@google.com (2026-03-16)

Project: chromium/src  

Branch:  main  

Author:  Camillia Smith Barnes [cammie@chromium.org](mailto:cammie@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7664083>

Shared Storage: Fix cross-entry state carry-over in origin matching

---


Expand for full commit details
```
     
    This commit fixes a logic bug in 
    `SharedStorageWorkletHost::OnJsonParsed` where the `script_origin_match` 
    and `context_origin_match` flags were declared outside the loop that 
    iterates through the parsed JSON entries. Previously, a successful 
    origin match in an earlier entry could erroneously carry over its `true` 
    state to subsequent entries, potentially allowing invalid cross-origin 
    data opt-ins to pass validation. Moving these declarations inside the 
    loop ensures the match state is properly reset and evaluated 
    independently for each item in the list. 
     
    To prevent regressions, a new browser test, 
    `CrossOriginScript_Failure_CrossEntryCarryOver`, has been added to 
    `SharedStorageCreateWorkletCustomDataOriginBrowserTest`. This test 
    specifically validates the scenario where multiple origin configuration 
    entries are provided, ensuring that an earlier valid entry does not 
    incorrectly authorize a later invalid one when attempting to create a 
    worklet with a custom `dataOrigin`. 
     
    Bug: 488408915 
    Change-Id: Ie1d943413a713ca9b46476eb108ec9b73c67df00 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7664083 
    Reviewed-by: Yao Xiao <yaoxia@chromium.org> 
    Commit-Queue: Cammie Smith Barnes <cammie@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1599940}

```

---

Files:

- M `content/browser/shared_storage/shared_storage_browsertest.cc`
- M `content/browser/shared_storage/shared_storage_worklet_host.cc`

---

Hash: [296f628ddb68cc86bd5f26936afb5534a187d0b6](https://chromiumdash.appspot.com/commit/296f628ddb68cc86bd5f26936afb5534a187d0b6)  

Date: Mon Mar 16 16:20:05 2026


---

### sp...@google.com (2026-05-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Baseline. Exploitation Mitigation Bypass


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/488408915)*
