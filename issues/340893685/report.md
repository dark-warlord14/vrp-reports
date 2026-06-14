# Security: FedCM prompts do not show origin if initiator origin is opaque

| Field | Value |
|-------|-------|
| **Issue ID** | [340893685](https://issues.chromium.org/issues/340893685) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Identity>FedCM |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | cb...@chromium.org |
| **Created** | 2024-05-15 |
| **Bounty** | $2,000.00 |

## Description

#### SUMMARY

The FedCM prompts (either bubble or modal) will show `://` if the initiator origin is opaque.

This can result in origin spoofing, especially when combined with other issues.

Showing the FedCM prompt does not require user interaction.   

A compromised renderer can open popups without user interaction, so the PoCs dependent on popups can be performed with minimal user interaction.

The FedCM prompt has two dialog types [1]: bubble and modal. Both types are affected since they use the same logic to get the displayed origin string.

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/webid/fedcm_account_selection_view_desktop.h;l=52;drc=6f3f85b321146cfc0f9eb81a74c7c2257821461e>

#### VULNERABILITY DETAILS

The FedCM dialog uses `webid::FormatUrlForDisplay()` [1] to get the origin string to display. There are no checks for opaque origins in this function nor most of its callers, so opaque origins result in the string `://` being returned and displayed to users.

`webid::FormatUrlForDisplay()` is called by `FederatedAuthRequestImpl::FormatOriginForDisplay()` [2], which is called by either `GetTopFrameOriginForDisplay()` [3] or `GetIframeOriginForDisplay()` [4].

`GetTopFrameOriginForDisplay()` does not check if the origin is opaque.   

`GetIframeOriginForDisplay()` would return an error if the iframe origin is opaque, however, the code is currently hardcoded to skip this logic and always return `std::nullopt`.

`GetTopFrameOriginForDisplay()` is used when showing dialogs, such as `ShowAccountsDialog()` [5]. References of `GetTopFrameOriginForDisplay()` [4] also show it's used for error dialogs, loading dialogs, and other states.

`GetTopFrameOriginForDisplay()` is passed the origin from `GetEmbeddingOrigin()` [6], which always returns the main frame's last committed origin.

The origin isn't checked for opaqueness anywhere in the code path above.

[1] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/webid/webid_utils.cc;l=406;drc=8472105d014517b12911f76a93ddac5ba5bf371f>

[2] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/webid/federated_auth_request_impl.cc;l=324;drc=7e088bf159ef779ea494dd55bb48916be569b06a>

[3] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/webid/federated_auth_request_impl.cc;l=402;drc=7e088bf159ef779ea494dd55bb48916be569b06a>

[4] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/webid/federated_auth_request_impl.cc;l=414;drc=7e088bf159ef779ea494dd55bb48916be569b06a>

[5] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/webid/federated_auth_request_impl.cc;l=1714;drc=7e088bf159ef779ea494dd55bb48916be569b06a>

[6] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/webid/federated_auth_request_impl.cc;l=2770;drc=7e088bf159ef779ea494dd55bb48916be569b06a>

POTENTIAL SOLUTION

Check for origin opaqueness at one or more points in the code path shown above, and adjacent paths. If origin is opaque, return an error (assuming FedCM should be unsupported in opaque origins, as are other sensitive UIs that display origins).

#### VERSION

Chrome Version: 126.0.6478.3 Canary, 124.0.6367.208 Stable.

Operating System: Windows 10 Version 22H2 (Build 19045.4170)

#### BISECT

Starts reproducing on commit <https://chromium.googlesource.com/chromium/src/+/ea6193f7caf0dab0216461b2e05ae5769d777274>

Landed in 109.0.5361.0 in October 2022: <https://chromiumdash.appspot.com/commit/79d9b185bf4115c2bc6cbe919655f7a4cb940f24>

Verified repro down to 109.0.5361.0.

Prior to the commit above, the hostname (`aogarantiza.com`) is shown, which I don't think is correct either given the page's origin is opaque. That behavior probably exists since the introduction of FedCM.

#### REPRODUCTION CASE

Setup:

1. Run a simulated IDP server: `node server-single-account.js` (attached)

In real scenarios, an attacker would use a legit IDP since they would want real credentials.

##### Scenario 1: Using bubble dialog (`mode: widget`)

1. Navigate to <https://aogarantiza.com/chromium/fedcm-opaque.php>
2. Login using FedCM dialog

##### Scenario 2: Using modal dialog (`mode: button`)

Note: This requires an origin trial for FedCM button mode, which I registered for `aogarantiza.com` with 3P support.

1. Navigate to <https://aogarantiza.com/chromium/fedcm-opaque.php?mode=button>
2. Click anywhere once
3. Login using FedCM dialog

##### Scenario 3: Using popup to show prompt over another origin

1. Navigate to <https://alesandroortiz.com/security/chromium/fedcm-opaque-open.html>
2. Click anywhere once
3. Login using FedCM dialog

For all scenarios:

Observed: Origin of initiator is shown as `://`. Page is able to obtain credentials after successful login.

Expected: FedCM dialog is not shown.

#### CREDIT INFORMATION

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- [server-single-account.js](attachments/server-single-account.js) (text/javascript, 2.3 KB)
- [fedcm-opaque.php](attachments/fedcm-opaque.php) (application/x-httpd-php, 1.7 KB)
- [fedcm-opaque-open.html](attachments/fedcm-opaque-open.html) (text/html, 597 B)
- [fedcm-opaque-popup.php](attachments/fedcm-opaque-popup.php) (application/x-httpd-php, 863 B)
- [fedcm-opaque-origin.mp4](attachments/fedcm-opaque-origin.mp4) (video/mp4, 3.4 MB)
- fedcm-opaque-chained.png (image/png, 486.9 KB)

## Timeline

### al...@alesandroortiz.com (2024-05-15)

When chained with [issue 338233148](https://issues.chromium.org/issues/338233148), an origin spoof is more believable due to the placement of the FedCM prompt.

To test with that issue, follow Scenario 3 repro steps and move the popup window to the top of your screen (and optionally resize). See attached screenshot.

### al...@alesandroortiz.com (2024-05-15)

> Showing the FedCM prompt does not require user interaction.

Minor correction: Showing the FedCM bubble dialog does not require user interaction, but showing the FedCM modal dialog does require user interaction (enforced by renderer).

### el...@chromium.org (2024-05-16)

Security shepherd: thanks for the report. I have not tried to reproduce this locally but the report looks legit so I'm going to kick this to someone from FedCM for further triage. I'm provisionally setting Pri-2 Sev-2 since I think this would still require a user gesture to get anything of value.

### al...@alesandroortiz.com (2024-05-16)

Thanks for triage.

Minor correction: ChromiumDash link in report should be <https://chromiumdash.appspot.com/commit/ea6193f7caf0dab0216461b2e05ae5769d777274>

### cb...@chromium.org (2024-05-16)

I'm not sure what the best way to fix this is. What do we display elsewhere for opaque origins? Or maybe we should disallow using FedCM from an opaque origin?

cc'ing estark in case she has opinions on what origin we should show

### al...@alesandroortiz.com (2024-05-16)

Opaque origins aren't allowed to show permission prompts, device choosers, and other sensitive UI that requires an origin to be displayed. In other instances, a precursor origin may be appropriate if available and not opaque, but IMO in this instance it should be disallowed.

For reference, see [issue 40061374](https://issues.chromium.org/issues/40061374) `Security: Device chooser dialogs do not show origin if initiator origin is opaque`

### np...@google.com (2024-05-16)

I think rejecting FedCM if RP is opaque makes sense. Is it possible for IDP origin to be opaque? I didn't see that in the repro, I hope not

### cb...@chromium.org (2024-05-16)

IDP origin can't be opaque. <https://source.chromium.org/chromium/chromium/src/+/main:services/network/public/cpp/is_potentially_trustworthy.cc;drc=c0265133106c7647e90f9aaa4377d28190b1a6a9;l=287>

### al...@alesandroortiz.com (2024-05-16)

I don't think the IDP origin can be opaque for a couple of reasons:

1. The IDP isn't attacker-controlled and isn't rendered as a page when the RP uses the FedCM flow, making it impossible to be opaque AFAICT (unless *maybe* an AITM attack messes with response headers, which is already a high bar). An attacker would want to use a legitimate IDP to obtain credentials, and I can't see a scenario where showing an opaque IDP origin would help an attacker if the IDP is also attacker controlled.
2. The logic cited in report uses the attacker-provided `configURL` as the basis for the IDP origin displayed in the FedCM dialogs. Since `configURL` must point to a valid URL for the FedCM flow to work, barring another vulnerability, there isn't a way for an attacker to make the FedCM flow work while using an invalid `configURL` that doesn't get displayed properly.

### al...@alesandroortiz.com (2024-05-16)

Re: [#comment9](https://issues.chromium.org/issues/340893685#comment9), thanks for confirming. For reference, FedCM calls that in <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/webid/federated_auth_request_impl.cc;l=919;drc=c0265133106c7647e90f9aaa4377d28190b1a6a9>

### pe...@google.com (2024-05-17)

Setting milestone because of s2 severity.

### ap...@google.com (2024-05-21)

Project: chromium/src
Branch: main

commit a3a16c8a83373cca7390a5ab3d904577c115db9c
Author: Christian Biesinger <cbiesinger@chromium.org>
Date:   Tue May 21 15:26:33 2024

    [FedCM] Disallow opaque RP origins
    
    Bug: 340893685
    Change-Id: I6a653e2ab8b2d879411c700185a4cb34ea2b0f38
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5544746
    Reviewed-by: Joe Mason <joenotcharles@google.com>
    Auto-Submit: Christian Biesinger <cbiesinger@chromium.org>
    Reviewed-by: Andrey Kosyakov <caseq@chromium.org>
    Commit-Queue: Joe Mason <joenotcharles@google.com>
    Reviewed-by: Nicolás Peña <npm@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1303777}

M       content/browser/devtools/devtools_instrumentation.cc
M       content/browser/webid/fedcm_metrics.h
M       content/browser/webid/federated_auth_request_impl.cc
M       content/browser/webid/webid_utils.cc
M       third_party/blink/public/devtools_protocol/browser_protocol.pdl
M       third_party/blink/public/mojom/devtools/inspector_issue.mojom
A       third_party/blink/web_tests/external/wpt/credential-management/fedcm-opaque-rp-origin.https.html
A       third_party/blink/web_tests/external/wpt/credential-management/fedcm-opaque-rp-origin.https.html.headers
A       third_party/blink/web_tests/external/wpt/credential-management/support/fedcm-helper.sub.js.headers
M       tools/metrics/histograms/enums.xml

https://chromium-review.googlesource.com/5544746


### pe...@google.com (2024-05-22)

Merge rejected: M126 is already shipping to beta and this issue is marked as a Priority:P2,P3 or Type:feature request.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), ceb (ChromeOS), srinivassista (Desktop)

### cb...@chromium.org (2024-05-22)

As a security issue, it should not have been marked P2. Trying again.

### al...@alesandroortiz.com (2024-05-22)

Verified as fixed in 127.0.6494.0 Canary.

### am...@chromium.org (2024-06-14)

Since this is a fix for a medium severity issue and M126 is already shipping to Stable channel, declining merge to M126 Stable and this fix will ship in M127 Stable.

### sp...@google.com (2024-06-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
$1500 for report of low impact security UI spoofing + $500 partial bisect bonus


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-27)

Congratulations Alesandro! Given the rather low impact and potential for user harm, we have decided to award this issue $1,500 with an additional $500 for this partial bisect. It was a very detailed report and we appreciate that and your efforts in discovering and reporting this issue to us.

### al...@alesandroortiz.com (2024-06-27)

Thanks for the reward!

### pe...@google.com (2024-08-29)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/340893685)*
