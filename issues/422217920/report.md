# Lookalike protection is not applited to top-level redirects of Blob URIs, allowing URL spoofing via Googlelogoligatures

| Field | Value |
|-------|-------|
| **Issue ID** | [422217920](https://issues.chromium.org/issues/422217920) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>LookalikeChecks |
| **Platforms** | Android |
| **Reporter** | he...@gmail.com |
| **Assignee** | en...@google.com |
| **Created** | 2025-06-04 |
| **Bounty** | $10,000.00 |

## Description

#### VULNERABILITY DETAILS

It was discovered that Chrome's lookalike URL protections can be bypassed using blob: URLs from within iframes. This is a variation of [bug 391788835](https://issues.chromium.org/issues/391788835) (<https://chromium-review.googlesource.com/c/chromium/src/+/6227546>), where the original fix failed to account for the following:

1. Chrome allows lookalike URLs to be rendered inside iframes, as the origin is not visible to the user.
2. A blob: URI inherits the origin of the page that created it.
3. Lookalike checks are not applied to top-level navigations involving blob: URIs.

By combining these factors, an attacker can host a page on a benign domain and embed a lookalike domain within a sandboxed iframe using the allow-top-navigation attribute.

The iframe can then generate a blob: URL containing spoofed content and redirect the top-level window to it. Since blob: URLs bypass the lookalike protection, this allows for the creation of convincing phishing pages using visually similar ligatures (e.g., glogoligature, ologoligature, llogoligature, elogoligature).

A potential fix would be to extend lookalike URL checks to include navigations involving the blob: scheme.

I have also attached a video reproducing the attack (repro.mp4).

#### BISECT

The issue originates from <https://chromium-review.googlesource.com/c/chromium/src/+/1388562>, where a decision was made to skip lookalike checks for non-HTTP/HTTPS URLs.

Subsequently, in <https://chromium-review.googlesource.com/c/chromium/src/+/4163999>, the lookalike detection logic was moved to `chrome/browser/lookalikes/lookalike_url_service.cc`, where it currently resides.

```
if (!url.SchemeIsHTTPOrHTTPS() || net::HostStringIsLocalhost(url.host()) ||
  net::IsHostnameNonUnique(url.host()) ||
  lookalikes::GetETLDPlusOne(url.host()).empty() ||
  lookalikes::IsSafeTLD(url.host())) {
return result;
}

```
#### VERSION

Chrome Version: 136.0.7103.125 (Stable).   

Chrome Version: 138.0.7204.3 (Beta).   

Chrome Version: 139.0.7205.3 (Dev).   

Chrome Version: 139.0.7218.0 (Canary).

Operating System: Android 13; Pixel 4 Build/TP1A.220624.014

#### REPRODUCTION CASE

##### Steps to reproduce locally

1. Download index.html and blob.html, and host them on your web server.
2. Register a subdomain/domain using one of the target ligatures (e.g., pologoligaturec.yourdomain.com) and configure its DNS A record to point to your server.
3. Ensure you replace *{{domain-with-ligature}}* in index.html with the subdomain/domain you created in step 2.
4. On a Pixel phone, navigate to http://*{{web\_server\_ip}}*/index.html.
5. A spoofed page rendering the ligature in the URL bar will appear, bypassing Chrome’s lookalike protection.

##### Simplified reproduction (hosted by me)

1. On a Pixel phone, visit <https://lbherrera.me/index-5100317621.html>.
2. A spoofed page with the accounts.g*ologoligature*ogle.com domain will be shown without any browser warning.

#### CREDIT INFORMATION

Reporter credit: Luan Herrera (@lbherrera\_)

## Attachments

- [blob.html](attachments/blob.html) (text/html, 1.3 KB)
- [index.html](attachments/index.html) (text/html, 359 B)
- [repro.mp4](attachments/repro.mp4) (video/mp4, 193.3 KB)

## Timeline

### he...@gmail.com (2025-06-04)

Just to clarify, this bypass isn't limited to protections related only to ligature-based lookalikes, it also works against other types of lookalikes.

##### Steps to reproduce:

1. Open <https://www.xn--80ak6aa92e.com>. You will notice that Chrome shows a lookalike warning interstitial.
2. Navigate to <https://example.org>.
3. Using DevTools, insert the following tag `<iframe src="https://www.xn--80ak6aa92e.com"></iframe>` into the DOM.
4. In the DevTools console, switch the JavaScript context to the iframe, and execute the script below:

```
let blob = new Blob(["bypass"], { type: "text/html" });
let url = URL.createObjectURL(blob);
top.location = url;

```

After completing these steps, the top-level page will be redirected to [www.xn--80ak6aa92e.com](http://www.xn--80ak6aa92e.com), bypassing the lookalike interstitial entirely.

### sk...@google.com (2025-06-04)

Thank you for the bug report!

Mustafa - can you PTAL? I haven't reproduced, but the report mentions that the bug is live in Canary M139 and the attached video shows the bug in action.

### ch...@google.com (2025-06-05)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-06-05)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### me...@google.com (2025-06-05)

Thanks for the report again.

There are two independent issues here:

1. We aren't applying ligature (or lookalike) checks to non-https URLs
2. The omnibox is not properly aligning the blob url

IMO, the main issue is (2) because it effectively allows bypassing other lookalike checks too. For example, we show a warning for edit distance lookalikes like goog1e[.]com. However, omnibox will align the URL so that blob: is hidden, so the user will see ...goog1e.com.

However, as an immediate fix, we can apply ligature checks to all schemes.

### me...@google.com (2025-06-18)

It looks like (2) is previously reported in [bug 355143151](https://issues.chromium.org/issues/355143151) for desktop.

cc cthomp who owns that bug

### ct...@chromium.org (2025-06-18)

I think one key bit that is demonstrated here (but not in [Issue 355143151](https://issues.chromium.org/issues/355143151)) is how an attacker could do the cross-origin top level blob: navigation and thus actually bypass ever showing the lookalike warning (using the iframe trick to then navigate the top-level to the blob: URL). So thank you for putting in the effort to put together a good POC for this :-)

I think in this case on Android the URL elision is working correctly -- we are showing the effective origin of the blob: URL and eliding from the leading (least-significant) end. The blob: part is not the interesting bit, since blob: URLs carry origin information. However, the ligature makes that origin display spoofable.

### ch...@google.com (2025-07-03)

meacer: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ha...@google.com (2025-07-21)

[Bulk Edit] Friendly reminder that this bug is marked as a M139 release blocker and M139 stable cut is next week on July 29. PTAL asap and request a merge as soon as possible.

### am...@chromium.org (2025-07-29)

This issue goes back for sometime and was not a regression introduced in M139; therefore, this issue is not RBS for M139

### an...@chromium.org (2025-07-29)

[security shepherd]: Hi meacer@, what should be the next steps to resolve this issue? IIUC, cthomp@ thinks that item 2 in c#6 (URL elision) is WAI?

### me...@google.com (2025-07-29)

The current idea is to disable ligatures in the omnibox altogether, but that's not specifically to fix this issue. I have a proof of concept to do this, I need to productionize the CL.

### ch...@google.com (2025-07-31)

meacer: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-08-04)

We commit ourselves to a 60 day deadline for fixing for s1 severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

### ch...@google.com (2025-08-15)

meacer: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-08-30)

meacer: Uh oh! This issue still open and hasn't been updated in the last 44 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-09-14)

meacer: Uh oh! This issue still open and hasn't been updated in the last 59 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### xi...@chromium.org (2025-09-16)

[secondary security shepherd] Setting severity to S2 to be aligned with the other bug and the general severity guidelines (https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#TOC-Medium-severity).

### ch...@google.com (2025-09-29)

meacer: Uh oh! This issue still open and hasn't been updated in the last 74 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-10-14)

meacer: Uh oh! This issue still open and hasn't been updated in the last 89 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-10-29)

meacer: Uh oh! This issue still open and hasn't been updated in the last 104 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-11-13)

meacer: Uh oh! This issue still open and hasn't been updated in the last 119 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-11-28)

meacer: Uh oh! This issue still open and hasn't been updated in the last 134 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-12-13)

meacer: Uh oh! This issue still open and hasn't been updated in the last 149 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-12-28)

meacer: Uh oh! This issue still open and hasn't been updated in the last 164 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-01-12)

meacer: Uh oh! This issue still open and hasn't been updated in the last 179 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-01-27)

meacer: Uh oh! This issue still open and hasn't been updated in the last 194 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### me...@google.com (2026-01-29)

A fix actually landed for this in M144 for omnibox: <https://chromium-review.googlesource.com/c/chromium/src/+/7199504>

The original site for this report isn't up, but googlelogoligature.mustafaeacer.com doesn't show the ligatures.

ender: Since you landed the fix, would you mind me assigning this to you to mark it as closed? Thanks!

### en...@google.com (2026-01-29)

thanks Mustafa! marking as fixed since we suppressed ligatures.

### ch...@google.com (2026-01-29)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2026-02-13)

ender: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### sp...@google.com (2026-03-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
High impact security UI spoof


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-05-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/422217920)*
