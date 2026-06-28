# Security: Download UI and address bar spoof with Google Sans font ligatures (similar to issue 391788835)

| Field | Value |
|-------|-------|
| **Issue ID** | [418273622](https://issues.chromium.org/issues/418273622) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Android |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | me...@chromium.org |
| **Created** | 2025-05-16 |
| **Bounty** | $5,000.00 |

## Description

## SUMMARY

Similar to [issue 391788835](https://issues.chromium.org/issues/391788835), the Google Sans font ligatures can be used to spoof origin in Download UI after download ("File downloaded" banner + Downloads page). If download URL is opened in a new tab, the spoofed origin is also shown in the address bar during confirmation prompts.

## VULNERABILITY DETAILS

Affected UIs:

- Download banners (such as the "File downloaded" confirmation message)
- Download page
- Address bar, if download URL is opened in new tab and prompts are shown (such as "Download file again?" prompts)

## VERSION

Verified repro on these versions:

Chrome version: 136.0.7103.87 Stable, 137.0.7151.23 Beta, 138.0.7178.0 Dev, 138.0.7180.0 Canary

Operating System: Android 14, Android 15

## REPRODUCTION CASE

Setup:
Make your Android device resolve `googlelogoligature.com` to your malicious server that hosts a downloadable file. In my case, my router let me override DNS entries so it's easy to test on physical device. For emulated devices, not sure if host's DNS resolution would affect the emulated devices.

Note: For this PoC, we use HTTP instead of HTTPS because we didn't set up a cert for `googlelogoligature.com` or any of the other spoofs. This also causes the "File can't be downloaded securely" prompt. An attacker *can* get a valid cert for the actual domain, so these are limitations that exist only in this PoC, not real attacks.

Note: download.zip on my server is a benign file with only the string "empty".

### Scenario 1: Download in same tab (\_self)

1. Navigate to <http://plain.text.aogarantiza.com/chromium/ligatures-download.html>
2. Wait a few moments (will trigger download for <http://googlelogoligature.com/download.zip>).
3. (For this PoC, click "Keep" in the "File can't be downloaded securely" prompt.)
4. Optional: Click a `_self` download link to trigger another download.

Observed: "File downloaded" banner and download page show spoofed origin (with font ligature).

Expected: "File downloaded" banner and Download page show actual origin.

### Scenario 2: Download in new tab (\_blank)

1. Navigate to <http://plain.text.aogarantiza.com/chromium/ligatures-download.html>
2. Click a `_blank` download link to trigger download in new tab.

Observed: While prompts are shown, address bar shows spoofed origin. After download, "File downloaded" banner and download page show spoofed origin (with font ligature).

Expected: While promtps are shown, address bar shows actual origin. After download, "File downloaded" banner and Download page show actual origin.

## Credit Information

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- [ligatures-download.html](attachments/ligatures-download.html) (text/html, 1.7 KB)
- [ligatures-download.mp4](attachments/ligatures-download.mp4) (video/mp4, 9.9 MB)

## Timeline

### an...@chromium.org (2025-05-16)

meacer@ would you mind taking a look?

### al...@alesandroortiz.com (2025-05-17)

This spoof also works with all the other ligatures identified in [issue 391788835](https://issues.chromium.org/issues/391788835). Pasting here for easier reference.

"googlelogoligature",
"glogoligature",
"ologoligature",
"llogoligature",
"elogoligature",
"g\_logo",
"o\_logo",
"l\_logo",
"e\_logo",
"google\_logo",
"google\_g",
"super\_g\_logo"

### al...@alesandroortiz.com (2025-05-18)

Download notification formats URL in `DownloadUtils.formatUrlForDisplayInNotification()`. [1]

See comments in related [issue 418214610](https://issues.chromium.org/issues/418214610) for some ideas on how to fix. Not sure if fixes discussed there will work or are appropriate for address bar, though.

[1] <https://source.chromium.org/chromium/chromium/src/+/main:components/browser_ui/util/android/java/src/org/chromium/components/browser_ui/util/DownloadUtils.java;l=145;drc=c98562e7738f9064034d94e0fe748cc0ba2663cb>

### an...@chromium.org (2025-05-19)

I haven't repro'd myself because I can't set up the DNS override but the video is clear enough hopefully.
I have CC'd meacer@ as well since the address bar also shows the spoofed origin. Not sure if that will need to be tackled separately.

### ch...@google.com (2025-05-20)

Setting milestone because of s2 severity.

### ch...@google.com (2025-05-20)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### al...@alesandroortiz.com (2025-05-20)

I have a WIP patch in <https://issues.chromium.org/issues/418214610#comment18> for a related issue. Probably same technique can be used for this issue, so will upload CL for this issue within a few days.

### al...@alesandroortiz.com (2025-05-20)

So far, seems like patch from other issue partially fixes issue since Download UI also uses the same code path.

However, not sure if ZWNJ approach will work for address bar. In manual testing where I added ZWNJ character via keyboard, it converted the URL to punycode, which is not what happens when the ligature by itself is typed. Not sure if the same issue would occur if browser adds the ZWNJ character.

Therefore, address bar display may need need a separate fix but will take a look later this week. Ideas welcome on how to approach address bar display without breaking it too much.

### al...@alesandroortiz.com (2025-05-22)

<https://crrev.com/c/6576707> doesn't do anything for downloads UI, so this will require separate targeted fix for downloads UI. And not sure what we want to do with address bar.

Maybe we can also throttle download navigations, but not sure if this is always desirable. Will try to make that work before making any UI fixes.

### al...@alesandroortiz.com (2025-06-01)

I took a look at the behavior on desktop, and it seems there are two important differences:

1. In cases where there is a prompt (such as when save dialog is shown, with "Ask where to save each file before downloading" enabled), on desktop the URL in the address bar is blank. On Android, the download URL is shown.
2. The download source on desktop is the last-interacted origin or blank, as documented in these issues [1][2][3] that made desktop-only changes. On Android, the source seems to always be the download URL.

For address bar: Hiding the URL in Android would mitigate the address bar spoof and match desktop behavior. But not sure which platform's behavior is preferred by the Chromium team; maybe we do want to show the URL. Hiding URL is easier and less risky than temporarily injecting ZWNJ into address bar when download confirmation prompt is shown.

For download UI: This might be fixable with targeted ZWNJ approach, similar to <https://crrev.com/c/6575322> but specific to affected download UI.

For both, showing top-level interstitial for downloads with spoofy URLs may also work, but not sure if downloads currently go through the lookalike throttle.

I'll see if downloads hit the lookalike throttle, and prototype that fix if it works. If not, I'll also try to prototype the other fixes. Open to any other ideas too.

[1] <https://crbug.com/40280033>

[2] <https://crbug.com/352681108>

[3] <https://crbug.com/417009057#comment3>

### al...@alesandroortiz.com (2025-06-02)

Turns out the lookalike throttle is called, but doesn't throttle downloads as expected.

I verified this bypass works with a valid cert, as mentioned in the original report. I used a modified build that throttles `aogarantiza.com` as a ligature spoof, in order to test with a valid certificate and exclude the possibility of SSL errors causing the lookalikes throttle bypass.

## Root Cause Analysis

### Summary

Download results in network error being set to `net::ERR_ABORTED` + `ErrorNavigationTrigger::kShouldNotRenderResponse`, lookalike throttle returns `PROCEED` if there's a network error, therefore lookalike throttle is bypassed.

### Details

Observed behavior based on logs:

In `NavigationRequest::OnResponseStarted()` [1], `response_should_be_rendered_` is false for downloads, therefore these variables are set: `net_error_ = net::ERR_ABORTED` (`-3`), `extended_error_code_ = ErrorNavigationTrigger::kShouldNotRenderResponse` (`8`) [2][3].

[1] <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_request.cc;l=4595;drc=736622ed7d9cf605750afa417b3f4e681eef686c>

```
  // Check if the response should be sent to a renderer.
  // Regular downloads should not be rendered, but downloads with an
  // unsuccessful response code will cause an error page to be rendered.
  response_should_be_rendered_ =
      (!is_download ||
       IsFailedDownload(is_download, response_head_->headers.get())) &&
      (!response_head_->headers.get() ||
       (response_head_->headers->response_code() != net::HTTP_NO_CONTENT &&
        response_head_->headers->response_code() != net::HTTP_RESET_CONTENT &&
        !ShouldRenderFallbackContentForResponse(*response_head_->headers)));

  if (!response_should_be_rendered_) {
    net_error_ = net::ERR_ABORTED;
    extended_error_code_ =
        static_cast<int32_t>(ErrorNavigationTrigger::kShouldNotRenderResponse);
    SelectFrameHostForOnResponseStarted(std::move(url_loader_client_endpoints),
                                        is_download,
                                        std::move(subresource_loader_params));
    return;
  }

```

[2] `ErrorNavigationTrigger::kShouldNotRenderResponse = 8` <https://source.chromium.org/chromium/chromium/src/+/main:tools/metrics/histograms/metadata/navigation/enums.xml;l=281;drc=92c781f85522ae317e72e560bd45b03cf5b43d11>

[3] `ErrorNavigationTrigger::kShouldNotRenderResponse` <https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_request.h;l=272;drc=5750b441369b022df43f1323d10375b5fd2a0565>

In `LookalikeUrlNavigationThrottle::WillProcessResponse()`, throttle will return `PROCEED` if there's a network error. This condition is met because `GetNetErrorCode()` returns `net::ERR_ABORTED` (`8`) due to the download logic above.

[4] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/lookalikes/lookalike_url_navigation_throttle.cc;l=210;drc=794461ea8634f85990135da95a47c3d235a56a42>

```
  // Ignore errors and same document navigations.
  if (handle->GetNetErrorCode() != net::OK || handle->IsSameDocument()) {
    return content::NavigationThrottle::PROCEED;
  }

```

I verified that not setting `net_error_` in `NavigationRequest::OnResponseStarted()` results in lookalike throttle blocking the request. I also verified that even if `net_error_` is set to non-OK, skipping the `return content::NavigationThrottle::PROCEED` in `LookalikeUrlNavigationThrottle::WillProcessResponse()` also results in lookalike throttle behaving blocking the request.

### Proposed fix

Modify the lookalike throttle to treat `ErrorNavigationTrigger::kShouldNotRenderResponse` pseudo-errors (or maybe only downloads) as normal navigations that should be throttled and have interstitial. This means the spoof still occurs in address bar and download UI, but only after user accepts the interstitial. This is the same mitigation approach used in other lookalike spoof bugs: warn user before, but if they accept risk through interstitial, there are no further mitigations.

I'll work on CL with this approach. I'll need to see how we can show an interstitial for downloads, because right now there is no interstitial shown if I bypass the network error check in the throttle (currently behaves like a status code `204` navigation).

### Further analysis

I may perform further analysis to see there are other network errors (or pseudo-errors) that result in lookalike throttle bypasses with security impacts.

### al...@alesandroortiz.com (2025-06-03)

Proposed patch to cancel throttled download request (but without showing interstitial):

In `LookalikeUrlNavigationThrottle::WillProcessResponse()`, change:

```
  // Ignore errors and same document navigations.
  if (handle->GetNetErrorCode() != net::OK || handle->IsSameDocument()) {

```

to

```
  // Ignore errors if not a download (see crbug.com/418273622). Also ignore same document navigations.
  if ((handle->GetNetErrorCode() != net::OK && !handle->IsDownload()) || handle->IsSameDocument()) {

```

That will cancel the request, essentially treating it as a `204` navigation where nothing happens. It works well on desktop and Android, but we're missing the interstitial.

I tried getting it to show the interstitial, but I wasn't successful. I think the issue I'm facing is we're setting `response_should_be_rendered_` to false early on in `OnResponseStarted()`, before we run the lookalike throttle, so the rest of the `NavigationRequest` assumes there won't be a response body. Then when we reach `WillProcessResponse()` and try to set a response body, things aren't in the correct state to serve a response. Some of my attempts either hit DCHECKs or crashed.

Logs show that `ShowInterstitial()` is being called, so I'm not sure why it's not being shown here. In case it's helpful, this is the state of `NavigationRequest` within `OnWillProcessResponseChecksComplete()` after the lookalike throttle is run: `action: 2 (CANCEL), isErrorPage? 0, didEncounterError? 1, IsDownload? 1, NetErrorCode: -3 (ERR_ABORTED), NetExtendedErrorCode() 8 (kShouldNotRenderResponse)`.

I'd appreciate any advice on how to get the interstitial shown. Alternatively, someone can also finish up the interstitial part of the patch. Without the interstitial, there is no user feedback on cancellation and no way for user to continue with the download if they really want to for some reason.

meacer@: Can you please take a look, or loop in someone who can?

### ch...@google.com (2025-06-03)

shaktisahu: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### al...@alesandroortiz.com (2025-06-03)

There's also the download from context menu ("Download link" in Android) scenario, where we want to make sure we show an interstitial or something else. With patched throttle, it fails silently.

That said, downloads currently fail silently if it's an insecure download from a secure page (e.g. `https://example.com` has link to `http://insecure.example.com/download.zip`). As a user, I personally have found it frustrating when I encounter cases like this that fail silently, but if it's acceptable for Chromium team, then we can also make lookalikes throttle silently.

The patch in [#comment13](https://issues.chromium.org/issues/418273622#comment13) would also throttle all lookalikes, not only ligatures. If we want downloads to only throttle for lookalike ligatures, then we can check if it's a download within `LookalikeUrlService`, similar to <https://chromium-review.googlesource.com/c/chromium/src/+/6576707/5/chrome/browser/lookalikes/lookalike_url_service.cc#216>

### al...@alesandroortiz.com (2025-06-04)

Re: [#comment13](https://issues.chromium.org/issues/418273622#comment13), I figured out how to get interstitial to show for downloads. :) Not sure if the best approach, but it seems to work. Will upload CL after further testing and cleanup.

### al...@alesandroortiz.com (2025-06-06)

Uploaded CL that only checks for lookalike ligatures: <https://crrev.com/c/6626322> (pending tests)

Unfortunately that doesn't handle direct context menu downloads (on Android or desktop), so will need to add ligature check to that code path as well, at least for it to fail silently.

If we want to surface block to user for direct downloads, then instead of throttling download navigations like in proposed CL, the download UI should be updated to check for lookalikes and show feedback to user much like Safe Browsing-flagged downloads are currently shown. Updating this UI is a much bigger CL (incl. new string localization). I'm concerned that showing `File comes from fake site \n Do you want to download file.apk anyway? [Cancel] [Download anyway]` in prompt on Android, or `Download from fake site blocked [Keep]` in downloads menu/page on desktop isn't too compelling for users to block the download, compared to full page interstitial with `Fake site ahead` full page interstitial.

Given the limited radius of the ligature spoof check (uncommon ligatures that are very unlikely to be used legitimately in the wild), I'm comfortable with silent blocks for this specific lookalike check, but it's ultimately up to the Chromium team.

### ch...@google.com (2025-06-18)

shaktisahu: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-07-03)

shaktisahu: Uh oh! This issue still open and hasn't been updated in the last 44 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-07-18)

shaktisahu: Uh oh! This issue still open and hasn't been updated in the last 59 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-08-02)

shaktisahu: Uh oh! This issue still open and hasn't been updated in the last 74 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-08-17)

shaktisahu: Uh oh! This issue still open and hasn't been updated in the last 89 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-09-01)

shaktisahu: Uh oh! This issue still open and hasn't been updated in the last 104 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-09-16)

shaktisahu: Uh oh! This issue still open and hasn't been updated in the last 119 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-10-01)

shaktisahu: Uh oh! This issue still open and hasn't been updated in the last 134 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-10-16)

shaktisahu: Uh oh! This issue still open and hasn't been updated in the last 149 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-10-31)

shaktisahu: Uh oh! This issue still open and hasn't been updated in the last 164 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-11-15)

shaktisahu: Uh oh! This issue still open and hasn't been updated in the last 179 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-11-30)

shaktisahu: Uh oh! This issue still open and hasn't been updated in the last 194 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-12-15)

shaktisahu: Uh oh! This issue still open and hasn't been updated in the last 209 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-12-30)

shaktisahu: Uh oh! This issue still open and hasn't been updated in the last 224 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ke...@chromium.org (2026-01-05)

shaktisahu@: This has been open for quite a while, and we've had a second vulnerability report submission for it. Is it something you're able to work on, or else can you help find a new owner for it?

### ch...@google.com (2026-01-14)

shaktisahu: Uh oh! This issue still open and hasn't been updated in the last 239 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-01-29)

shaktisahu: Uh oh! This issue still open and hasn't been updated in the last 254 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-02-13)

shaktisahu: Uh oh! This issue still open and hasn't been updated in the last 269 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-02-28)

meacer: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### me...@google.com (2026-03-13)

For review visibility

### ch...@google.com (2026-03-15)

meacer: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### me...@google.com (2026-03-16)

deleted

### me...@chromium.org (2026-03-16)

Fix is out for review at https://chromium-review.googlesource.com/c/chromium/src/+/7666049

### dx...@google.com (2026-03-16)

Project: chromium/src  

Branch:  main  

Author:  Mustafa Emre Acer [meacer@chromium.org](mailto:meacer@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7670344>

Disable ligatures for all message banners on Android

---


Expand for full commit details
```
     
    This change disables rendering of ligatures in message banners for security and readability. Similar changes were previously made 
    for the omnibox (crrev.com/c/7199504) and permission dialogs (crrev.com/c/7536052). 
     
    Bug: 418273622 
    Change-Id: I881b013b9b341b889fe764071623247ab41bf7f6 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7670344 
    Commit-Queue: Mustafa Emre Acer <meacer@chromium.org> 
    Reviewed-by: Matthew Jones <mdjones@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1600082}

```

---

Files:

- M `components/messages/android/internal/BUILD.gn`
- M `components/messages/android/internal/java/src/org/chromium/components/messages/MessageBannerCoordinator.java`

---

Hash: [30d6ec8cc044a5cbfb77e08d32c1d8b6edaef76c](https://chromiumdash.appspot.com/commit/30d6ec8cc044a5cbfb77e08d32c1d8b6edaef76c)  

Date: Mon Mar 16 20:25:11 2026


---

### sp...@google.com (2026-06-08)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
High Quality. Security UI Spoofing.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/418273622)*
