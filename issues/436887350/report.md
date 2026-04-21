# Security: Extension can download file by resuming interrupted download

| Field | Value |
|-------|-------|
| **Issue ID** | [436887350](https://issues.chromium.org/issues/436887350) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Linux, Windows, ChromeOS |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | qi...@google.com |
| **Created** | 2025-08-06 |
| **Bounty** | $4,000.00 |

## Description

## SUMMARY

An extension with `downloads` permission can download a `file://` URL by calling `downloads.download()`, waiting for the download to be interrupted, and then calling `downloads.resume()` on the interrupted download. This causes the download to be initiated by the browser, bypassing `DownloadRequestUtils::IsURLSafe()`/`CPSP::CanRequestURL()` checks.

Downloading local files is meant to be blocked when the extension does not have `file://` permissions. The `tabs.create()` workaround to download some local files was also blocked in <https://crrev.com/c/4772028> (August 2023, also see [issue 40063229](https://issues.chromium.org/issues/40063229)).

The resume bypass also works with all other ways to resume downloads, including resumes made through UI.

When chained with other bugs, such as [issue 433800617](https://issues.chromium.org/issues/433800617) or [issue 435684924](https://issues.chromium.org/issues/435684924), or if the attacker otherwise convinces user to upload the downloaded file, the attacker can steal the downloaded file's contents.

## VULNERABILITY DETAILS

In [`DownloadManagerImpl::BeginDownloadInternal()`](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/download/download_manager_impl.cc;l=1520;drc=877c4eff05eee91a64ab498b2f02928fe718278b)...

```
void DownloadManagerImpl::BeginDownloadInternal(
    std::unique_ptr<download::DownloadUrlParameters> params,
    scoped_refptr<network::SharedURLLoaderFactory> blob_url_loader_factory,
    bool is_new_download,
    const std::string& serialized_embedder_download_data) {
  // Check if the renderer is permitted to request the requested URL.
  if (params->render_process_host_id() >= 0 &&
      !DownloadRequestUtils::IsURLSafe(params->render_process_host_id(),
                                       params->url())) {
    CreateInterruptedDownload(
        std::move(params),
        download::DOWNLOAD_INTERRUPT_REASON_NETWORK_INVALID_REQUEST,
        weak_factory_.GetWeakPtr());
    return;
  }
  // ...
}

```

...`CPSP::CanRequestURL()` is called through [`DownloadRequestUtils::IsURLSafe()`](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/download/download_request_utils.cc;l=31;drc=27f899da22267983fb22a8caf88d300a9d49cf3d) only if `render_process_host_id() >= 0`.

When `downloads.download()` is called with a `file://` URL, `render_process_host_id` is greater than zero, and `CPSP::CanRequestURL()` returns false for `file://` URLs, therefore the download is interrupted.

However, when `downloads.resume()` is called for the interrupted download, `render_process_host_id` is `-1`, which per [this comment](https://source.chromium.org/chromium/chromium/src/+/main:components/download/public/common/download_url_parameters.h;l=305;drc=877c4eff05eee91a64ab498b2f02928fe718278b) means it's not associated with a frame. This means the `IsURLSafe()`/`CPSP::CanRequestURL()` check is bypassed, and the file is downloaded.

### Additional context

In the `DownloadUrlParameters()` constructor that leaves `render_process_host_id` at `-1`, there is [this comment](https://source.chromium.org/chromium/chromium/src/+/main:components/download/public/common/download_url_parameters.h;l=78;drc=877c4eff05eee91a64ab498b2f02928fe718278b) that points out the security checks bypass:

```
  // Constructs a download not associated with a frame.
  //
  // It is not safe to have downloads not associated with a frame and
  // this should only be done in a limited set of cases where the download URL
  // has been previously vetted. A download that's initiated without
  // associating it with a frame don't receive the same security checks
  // as a request that's associated with one. Hence, downloads that are not
  // associated with a frame should only be made for URLs that are either
  // trusted or URLs that have previously been successfully issued using a
  // non-privileged frame.
  DownloadUrlParameters(
      const GURL& url,
      const net::NetworkTrafficAnnotationTag& traffic_annotation);

```

Unfortunately, this constructor is used in the `downloads.resume()` code path and most other download resume code paths: [`DownloadsResumeFunction::Run()`](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/extensions/api/downloads/downloads_api.cc;l=1297;drc=27f899da22267983fb22a8caf88d300a9d49cf3d) calls `DownloadItem::Resume()` which calls [`DownloadItemImpl::ResumeInterruptedDownload()`](https://source.chromium.org/chromium/chromium/src/+/main:components/download/internal/common/download_item_impl.cc;l=2543;drc=877c4eff05eee91a64ab498b2f02928fe718278b).

`ResumeInterruptedDownload()` has [this comment](https://source.chromium.org/chromium/chromium/src/+/main:components/download/internal/common/download_item_impl.cc;l=2592;drc=877c4eff05eee91a64ab498b2f02928fe718278b) explaining why the unsafe constructor is used for resumes:

```
  // Avoid using the WebContents even if it's still around. Resumption requests
  // are consistently routed through the no-renderer code paths so that the
  // request will not be dropped if the WebContents (and by extension, the
  // associated renderer) goes away before a response is received.
  std::unique_ptr<DownloadUrlParameters> download_params(
      new DownloadUrlParameters(GetURL(), traffic_annotation));

```
## BISECT

Likely [commit 00b621f5126d538df488090c19175ee892a7161b](http://crrev.com/00b621f5126d538df488090c19175ee892a7161b) (February 2016) which starts using the unsafe constructor in resume code path.

I'll verify bisect later today.

## VERSION

Chrome version: 139.0.7258.67 Stable, 141.0.7340.0 Canary

Operating System: Windows 10

## REPRODUCTION CASE

To download a file in a user directory, the PoC first makes a throwaway download to get the username from the download path. Then we make the second download exploiting the vulnerability.

The core vulnerability itself doesn't need user interaction to download the file, nor does it need to show an extension page or otherwise open a new tab.

I'll upload chained scenarios in comments.

Setup:

1. Install attached extension: `manifest.json`, `background.js`, `page.html`, `page.js`.
2. Disable `file://` URL access in the extension details page (this is enabled by default for unpacked extensions).

### Scenario 1: Chrome history file

1. Click extension icon to trigger download. (Note: Initiating/resuming downloads doesn't require user interaction, so this step is only for PoC.)
2. Click the page, then select the downloaded file. (Note: When chained, we don't need user to explicitly upload file.)

Observed: Extension can download `file://` URLs without file permission. When chained with other vulns, or through social engineering, user can read downloaded local file.

Expected: Extension cannot download `file://` URLs without file permission.

### Debug scenario

To see the attack occurring more slowly, you can modify `background.js` and set `debug` to `true`, which delays the `resume()` call by two seconds. Reminder: Disable `file://` access in extension for proper repro.

## Credit Information

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- manifest.json (application/json, 354 B)
- background.js (text/javascript, 2.2 KB)
- page.html (text/html, 632 B)
- page.js (text/javascript, 700 B)
- download-file-resume.mp4 (video/mp4, 1.4 MB)
- download-file-resume-debug.mp4 (video/mp4, 1.6 MB)
- manifest.json (application/json, 385 B)
- background.js (text/javascript, 2.5 KB)
- page.html (text/html, 659 B)
- page.js (text/javascript, 1.1 KB)
- download-file-resume-chained-cr.mp4 (video/mp4, 785.4 KB)

## Timeline

### al...@alesandroortiz.com (2025-08-06)

Actually, at the time when commit 00b621f5126d538df488090c19175ee892a7161b was made (Feb 2016) it seems `file://` downloads were allowed anyway, so it was at some point after that `CanRequestURL()` and `file://` checks were added. But generally, this repros into ancient history (the UI looked so different back then!).

### al...@alesandroortiz.com (2025-08-06)

Minor correction on repro's expected state: "...user can read downloaded file" -> "...attacker can read downloaded file"

### al...@alesandroortiz.com (2025-08-06)

PoC chained with [issue 433800617](https://issues.chromium.org/issues/433800617) below. This can alternatively be chained with [issue 435684924](https://issues.chromium.org/issues/435684924) which is very similar, so I won't provide separate chained PoC for the second issue since behavior and impact is basically the same as shown in PoC below.

The PoC uses an extension page, but the chained part (uploading the file) can be done from a compromised renderer on any page (with or without content script).

## REPRODUCTION CASE

Setup:

1. Apply patch from [issue 433800617](https://issues.chromium.org/issues/433800617) and build Chromium (only parts of the patch from `third_party/blink/renderer/core/html/forms/file_input_type.cc` are needed, but you can apply full patch.)
2. Install attached extension: `manifest.json`, `background.js`, `page.html`, `page.js`.
3. Disable `file://` URL access in the extension details page (this is enabled by default for unpacked extensions).

### Scenario 2: Chained with [issue 433800617](https://issues.chromium.org/issues/433800617) to minimize user interaction

See [issue 433800617](https://issues.chromium.org/issues/433800617) for full context on happy/sad paths.

Using patched browser:

1. Click extension icon to open extension page. (Note: Opening extension page doesn't need user interaction, so this step is only for PoC.)
2. Press and hold enter.

- For happy path: Wait for attack to complete within a couple of seconds.
- For sad path (non-downloads folder case): Select downloads folder, then click "Open" button.

Observed: Extension can download `file://` URLs without file permission. When chained with [issue 433800617](https://issues.chromium.org/issues/433800617) (or similar issues like [issue 435684924](https://issues.chromium.org/issues/435684924)), attacker can read downloaded local file with minimal user interaction (holding enter).

Expected: Extension cannot download file:// URLs without file permission.

### za...@google.com (2025-08-07)

Thank you for the detailed report. It seems the core issue is a permission bypass in the download resumption logic. As you've identified, a download resumed via downloads.resume() is not associated with a renderer process (render\_process\_host\_id = -1), which causes the IsURLSafe() security check to be skipped. This allows an extension with only the downloads permission to download local file:// URLs it should not have access to. The chained impact, leading to arbitrary local file disclosure, makes this a security issue.

Triaging accordingly and routing to the Downloads for investigation.

Hi dtrainor@, can you take a look at this bug and assign to a correct eng if necessary? It seems like an attack can disclose the internal files to malicious extensions.

### ch...@google.com (2025-08-08)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-08-22)

dtrainor: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dt...@google.com (2025-09-02)

Yes reassigning to qinmin@ to investigate this week. Apologies for the delay!

### dx...@google.com (2025-09-02)

Project: chromium/src  

Branch:  main  

Author:  Min Qin [qinmin@chromium.org](mailto:qinmin@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6907509>

Fix an issue when determining whether a download is resumable in extension

---


Expand for full commit details
```
    extension 
     
    To resume a download, the download should be in an interrupted state, 
    rather than paused state. The current code will just always return 
    true and skip the canResume() check. 
     
    Bug: 436887350 
    Change-Id: Ie5cd0e7684a1eeacc4d80899098e89137dc1a85f 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6907509 
    Reviewed-by: David Trainor <dtrainor@chromium.org> 
    Commit-Queue: Min Qin <qinmin@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1509939}

```

---

Files:

- M `chrome/browser/extensions/api/downloads/downloads_api.cc`

---

Hash: [f9f478196e288d68bf0b64a30fa7618a27fe1fc2](https://chromiumdash.appspot.com/commit/f9f478196e288d68bf0b64a30fa7618a27fe1fc2)  

Date: Tue Sep 2 23:44:44 2025


---

### al...@alesandroortiz.com (2025-09-03)

Thanks for the CL, I'll check tomorrow on Canary.

Are there other CLs planned to mitigate other ways to resume downloads? The CL fixes the extension scenario, but not other ways to resume downloads as I mentioned in report:

> The resume bypass also works with all other ways to resume downloads, including resumes made through UI.

The most prominent ways are the "Try again" buttons in the downloads bubble and Downloads page. I don't know if there are additional ways to resume downloads, with or without user interaction.

### qi...@google.com (2025-09-03)

I think "try again" is working as intended. Download can be either browser initiated or renderer initiated.  I think "try again" should be classified as a browser initiated download, and thus shouldn't be subject to permission restrictions.

There are also some other cases that download can fail when triggering from a page, but will succeed if user retries or resumes on Chrome downloads page. For example, download can fail in cross-origin case. But if user copy and paste the URL in the omnibox, the download will succeed. As a result, if a download resumption is user initiated, we normally treat it as a browser initiated download and will resend the URL request.

### al...@alesandroortiz.com (2025-09-03)

An attacker could convince the user to click "try again" (or use a chained vuln to press it for the user; I'm reporting one soon), and since there isn't any source information or accurate information about the error in the downloads bubble, the user may still think it's a remote file instead of a local file.

It only adds one user interaction to the attack, so feels like something that should still be mitigated to avoid variant attacks. But if it may break existing behavior or will take significant work to implement (especially to make sure it's blocked only for initially-renderer-initiated downloads), then a fix for these other resume paths can be tracked separately with lower priority.

### ch...@google.com (2025-09-17)

qinmin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-10-02)

qinmin: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-10-06)

We commit ourselves to a 60 day deadline for fixing for s1 severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

### ch...@google.com (2025-10-07)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M140. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M141. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M142. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [140, 141, 142].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ts...@google.com (2025-10-07)

I'm not sure this meets the bar for a stable merge, however, let's get this merged to m142 (7444) after Weds 8-Oct but before Tues 14-Oct.

### ts...@google.com (2025-10-07)

Already in m142 which branched at refs/heads/main@{#1522585}

### sp...@google.com (2025-10-14)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $4000.00 for this report.

Rationale for this decision:
high quality medium impact exploit mitigation bypass


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### al...@alesandroortiz.com (2025-10-15)

Thanks for reward!

### al...@alesandroortiz.com (2025-10-16)

The extension scenario is verified as fixed (verified using bisect tool), but my concern about other ways to resume downloads still stands ([#comment10](https://issues.chromium.org/issues/436887350#comment10) and [#comment12](https://issues.chromium.org/issues/436887350#comment12)). Currently known attacks add additional mitigations (such as compromised renderer when chained with [issue 447172715](https://issues.chromium.org/issues/447172715)), but might be good to add as defense in depth in the future.

Thanks for fixing the main scenario!

### ch...@google.com (2026-01-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> high quality medium impact exploit mitigation bypass

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/436887350)*
