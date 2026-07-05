# Stale FedCM autofill suggestion triggers heap-use-after-free in the browser process via unchecked flat_map iterator dereference

| Field | Value |
|-------|-------|
| **Issue ID** | [494764370](https://issues.chromium.org/issues/494764370) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Identity>FedCM |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | cb...@chromium.org |
| **Created** | 2026-03-21 |
| **Bounty** | $3,000.00 |

## Description

# Stale FedCM autofill suggestion triggers heap-use-after-free in the browser process via unchecked flat\_map iterator dereference

## Summary

When a FedCM conditional mediation request is cancelled and a new request with a different identity provider is initiated, a previously displayed autofill suggestion from the old request remains clickable in the dropdown. Accepting this stale suggestion causes `RequestService::NotifyAutofillSuggestionAccepted` to look up the old IdP's config URL in `token_request_get_infos_`, which now only contains entries for the new request. The code dereferences the resulting past-end iterator without validation, producing a heap-use-after-free in the browser process. No source modifications are required to reproduce. Platform: all (tested on macOS arm64).

## Bisect

Introducing Commit: `1a0734c8e729d65d61d72414b52812af02a543d7`

- Date: 2025-04-22
- Author: Sam Goto
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/6472854>

## Root Cause

`RequestService::NotifyAutofillSuggestionAccepted` receives the IdP config URL from the autofill suggestion payload and searches for it in `token_request_get_infos_`, a `base::flat_map<GURL, IdentityProviderGetInfo>`. The result is used without checking whether the iterator equals `end()`:

```
// content/browser/webid/request_service.cc:1371-1381
auto get_info_it = token_request_get_infos_.find(idp);

if (!request_dialog_controller_->ShowLoadingDialog(
        CreateRpData(/*client_metadata_received=*/true),
        FormatOriginForDisplay(url::Origin::Create(idp)),
        get_info_it->second.rp_context, blink::mojom::RpMode::kActive,
        ...)) {
  return;
}

```

Other call sites in the same file guard the same map with `CHECK(it != end())`, confirming that the missing validation here is an oversight rather than a deliberate design choice:

```
// content/browser/webid/request_service.cc:571-572
auto idp_get = token_request_get_infos_.find(idp_config_url);
CHECK(idp_get != token_request_get_infos_.end());

```

The map is populated in `RequestToken` when a new FedCM request begins and cleared in `CleanUp` when a request completes or is cancelled. After cancellation and re-request with a different IdP, the map contains only the new IdP's entry, so a lookup for the old IdP's URL returns `end()`.

The stale suggestion persists because the autofill dropdown is a browser-side UI widget whose contents are populated when the user focuses on the input field. When the underlying FedCM request is cancelled, `CompleteRequestInternal` clears the request state but does not invalidate suggestions already displayed in the open dropdown. The `IdentityCredentialSuggestionGenerator` produces suggestions from accounts returned by `RequestService::GetAutofillSuggestions`, which queries the live request state; once the dropdown is open, however, its contents are not re-queried until the user defocuses and refocuses the field. A request switch that occurs while the dropdown remains open leaves the old suggestions intact and clickable.

`base::flat_map` is backed by a sorted `std::vector`. Dereferencing its `end()` iterator reads past the vector's logical size boundary. ASAN detects this as a heap-use-after-free because the vector's container overflow annotations poison the `[size(), capacity())` region.

The `show_modal` parameter that gates entry into the vulnerable code path is hardcoded to `true` in the sole caller, `AutofillExternalDelegate::DidAcceptSuggestion`, so every acceptance of an identity credential suggestion from the autofill dropdown reaches the unguarded `find()`.

The attack does not require the IdP to be local. An attacker who operates a legitimate FedCM identity provider (or compromises one) can serve a relying-party page that performs the request-cancel-re-request sequence entirely in JavaScript. The victim only needs to click a single autofill suggestion on the attacker's page. The PoC uses a localhost IdP for convenience, but the same flow works with any network-reachable IdP.

## Reproduce

Tested on commit `d0f83d769eeed` (macOS arm64). No source modifications required.

```
autoninja -C out/asan-release chrome

```

Start the fake IdP server:

```
python3 issue_fedcm_stale_suggestion/idp_server.py

```

Launch Chrome:

```
out/asan-release/Chromium.app/Contents/MacOS/Chromium \
  --disable-gpu --no-proxy-server \
  --enable-features=FedCmAutofill,AutofillNewSuggestionGeneration,FedCmWithoutWellKnownEnforcement,FedCmPreservePortsForTesting \
  --ignore-certificate-errors \
  --user-data-dir=/tmp/poc-$(date +%s) \
  --no-first-run --no-default-browser-check \
  'https://127.0.0.1:8443/set-login' 2>asan.log

```

Feature flags: `FedCmAutofill` and `AutofillNewSuggestionGeneration` enable FedCM identity suggestions in the autofill dropdown, which is the vulnerable code path. `FedCmWithoutWellKnownEnforcement` and `FedCmPreservePortsForTesting` allow the localhost IdP to operate on a non-standard port; these are test convenience flags and not required for the bug itself.

The page auto-redirects from `/set-login` (establishes IdP login status via the `Set-Login` response header) to `/poc.html`. Click the Email input field; an autofill dropdown appears showing "[user@idp-a.example](mailto:user@idp-a.example)". Wait approximately 3 seconds for the page log to show `[SWITCH] Request B started`, then click the stale suggestion. The browser process crashes immediately.

```
==70510==ERROR: AddressSanitizer: heap-use-after-free on address 0x60d000a45bd0 at pc 0x0001390d79c4 bp 0x00016b59d210 sp 0x00016b59d208
READ of size 4 at 0x60d000a45bd0 thread T0
    #0 ... in content::webid::RequestService::NotifyAutofillSuggestionAccepted(GURL const&, std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, bool, base::OnceCallback<void (bool)>)+0x1084
Address 0x60d000a45bd0 is a heap-use-after-free
SUMMARY: AddressSanitizer: heap-use-after-free in content::webid::RequestService::NotifyAutofillSuggestionAccepted(...)+0x1084
==70510==ABORTING

```

Full ASAN output is in `asan.log`.

## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [poc_demo.mp4](attachments/poc_demo.mp4) (video/mp4, 2.1 MB)
- [asan.log](attachments/asan.log) (text/plain, 39.8 KB)
- [readme.md](attachments/readme.md) (text/markdown, 1.6 KB)
- [poc.html](attachments/poc.html) (text/html, 1.8 KB)
- [idp_server.py](attachments/idp_server.py) (text/x-python, 5.0 KB)

## Timeline

### el...@google.com (2026-03-23)

Security shepherd: thanks for the report. I have not reproed this locally but I believe the report based on the attached ASAN log. I'm calling this Sev-0 since it's a web-reachable UaF with a fairly likely user gesture (clicking an autofill suggestion) and routing it based on that.

### el...@google.com (2026-03-23)

I *believe* this is Security\_Impact-None because FedCmAutofill is disabled, but cbiesinger@ please check me on that :)

### cb...@chromium.org (2026-03-24)

Yes FedCmAutofill is disabled

### cb...@chromium.org (2026-03-24)

should it still be S0 given that?

### el...@google.com (2026-03-24)

Since it's disabled, it's SecImpact-None which makes it SLO-exempt, but that doesn't affect the severity of the bug itself. Feel free to lower the priority below P0 though.

### dx...@google.com (2026-03-27)

Project: chromium/src  

Branch:  main  

Author:  Christian Biesinger [cbiesinger@chromium.org](mailto:cbiesinger@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7705015>

[FedCM] Make sure iterator is valid when autofill is accepted

---


Expand for full commit details
```
     
    If a FedCM request is aborted before the user accepts the 
    suggestion, the IDP will not be found in the map and, so 
    this CL checks for that. 
     
    Fixed: 494764370 
    Change-Id: I4ca99eb58f3bc3e5879d9b0065d28bea628fe4d6 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7705015 
    Commit-Queue: Christian Biesinger <cbiesinger@chromium.org> 
    Reviewed-by: Nicolás Peña <npm@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1606349}

```

---

Files:

- M `content/browser/webid/request_service.cc`
- M `content/browser/webid/request_service_unittest.cc`

---

Hash: [552ca56665e0ec9b287204862c2cb6e175a5acb0](https://chromiumdash.appspot.com/commit/552ca56665e0ec9b287204862c2cb6e175a5acb0)  

Date: Fri Mar 27 17:55:02 2026


---

### wf...@chromium.org (2026-04-02)

This is medium sev as it's a read of data that does not allow any code exec.

### sp...@google.com (2026-04-02)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Baseline User information disclosure with bisect


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/494764370)*
