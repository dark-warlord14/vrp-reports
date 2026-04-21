# Bypassing Mark of the Web with an HTML File and User Interaction

| Field | Value |
|-------|-------|
| **Issue ID** | [431309019](https://issues.chromium.org/issues/431309019) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Windows |
| **Reporter** | to...@gmail.com |
| **Assignee** | qi...@chromium.org |
| **Created** | 2025-07-12 |
| **Bounty** | $2,000.00 |

## Description

---

### Report description

Bypassing Mark of the Web with an HTML File and User Interaction

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

---

### The problem

#### Please describe the technical details of the vulnerability

### Vulnerability

A locally opened HTML file can be used to remove the Mark of the Web from any file accessible to the targeted user, including attacker-supplied executables.

### How?

Depending on whether a download is initiated by user interaction or generated via a data-src URL, the file will have different HostUrl values and ZoneIds.
Regardless of the ZoneID, the Mark of the Web can be fully removed simply by referencing the downloaded executable using its complete local path. This is only possible if the HTML file is opened locally via `file:///`.

### PoC

By referencing the downloaded file with its full path, for example `<iframe src="file:///C:/Users/<user>/Downloads/calc.exe">`, the browser will attempt to download the file again if it is an executable or a non-displayable file (such as a ZIP archive), instead of rendering its contents.

Instead of creating a new copy, the browser appears to overwrite the existing file, incorrectly treating it as a trusted local file. As a result, the Mark of the Web is removed from the payload.

You can retrieve the username in Chrome (with default settings) by reading `window.location.href` and extracting it with `match(/file:\/\/\/[a-zA-Z]:\/Users\/([^\/;]+)/i);`.

### Actual Bug that happens in background:

In Chrome, when downloading a file that already exists in the Downloads folder (referenced via its full path), the browser "overwrites" the original file instead of creating a copy. This overwriting removes the ADR (Alternate Data Stream) and, with it, the Mark of the Web.

Whether it really fully replaces the file with its full content or it just "strips" the ADR I am not sure of.

I believe, since the file is loaded via `file:///C:...` it is wrongly assumed as local origin. However, even if that were true, it should then, instead of omitting the ADR entirely, assign ZoneID 0.

More importantly, the ADR should be preserved: since the file originated from the internet and had MotW set, redownloading or referencing it locally should not strip the MotW.

Firefox
Firefox does not overwrite the file, so the MotW is not removed. Therefore, this method does not work in Firefox.

#### Impact analysis – Please briefly explain who can exploit the vulnerability, and what they gain when doing so

### What is the Impact?

**Security Feature Bypass – Mark of the Web**

This vulnerability enables attackers to distribute an HTML file containing an embedded executable payload. When a victim opens the HTML file and downloads the payload — either by clicking a link or through a delayed background download that avoids triggering the usual multiple-download permission popup — the payload can then be accessed and downloaded again using its full local file path. This second download strips the Mark of the Web (MotW) from the file. As a result, when the user is tricked into opening the file, no MotW is present and no security warning is displayed.

Exploiting this technique requires only basic technical skills.

For demonstration, two sample `motw.html` files are provided (one for ZoneId4 and one for ZoneId3, which triggers classic SmartScreen behavior), along with source code for a small executable, a template, and a PowerShell script to generate the `motw.html` file with the embedded executable (`calc.c` in `./src`). The executable simply launches `calc.exe`. The two HTML scenarios showcase different approaches: one leads to ZoneID 4, and the other to ZoneID 3. These files do not need to be hosted online; Chrome will automatically apply the Mark of the Web to any file downloaded via a local HTML file.

---

### The cause

#### Choose the type of vulnerability

Other

#### Does anyone else know about this vulnerability?

No, this vulnerability is private.

#### Do you plan to disclose this vulnerability publicly?

Yes, I plan to disclose

## Attachments

- Chrome-report.zip (application/x-zip-compressed, 15.5 MB)
- zone3.mp4 (video/mp4, 10.0 MB)
- zone4.mp4 (video/mp4, 9.1 MB)
- calc.c (text/x-csrc, 444 B)
- html_loader.ps1 (application/octet-stream, 481 B)
- template.html (text/html, 1.2 KB)
- zone4.html (text/html, 141.3 KB)
- deleted (application/octet-stream, 0 B)
- zone3.html (text/html, 141.6 KB)

## Timeline

### to...@gmail.com (2025-07-12)

### Tested Versions:

Google Chrome 138.0.7204.101 (Offizieller Build) (64-Bit) (cohort: Stable)
Windows 11 Version 23H2 (Build 22631.5472)

### ma...@google.com (2025-07-14)

Reporter, can you please attach all files uncompressed directly to this bug? Thank you!

### ma...@google.com (2025-07-15)

Thanks. Provisionally triaging this as a low severity issue.

Download folks, should download from a file:// URL create a new file instead of the existing one, perhaps? That would obviate any discussion on whether Chrome should go out of its way to keep the MoTW intact in this case.

### ch...@google.com (2025-07-15)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### dx...@google.com (2025-07-29)

Project: chromium/src  

Branch:  main  

Author:  Min Qin [qinmin@chromium.org](mailto:qinmin@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6758511>

Cancel download if target is the same as source

---


Expand for full commit details
```
     
    The original comments about disallowing a download if target is the same 
    as the source is from here: 
    https://chromium-review.googlesource.com/c/chromium/src/+/475792. 
    However, this CL doesn't seem to cancel or interrupt the download. 
    So this CL will do the cancelling of the download. This may have 
    some implications on file URLs since the target filepath may always 
    be the same as the the original path. An alternative is to always 
    uniquify the file path in that case. However, this doesn't solve 
    the issue that Chrome may stuck in a download loop to try to 
    auto-open an binary file->result in a download->auto-open again... 
     
    Bug: 431309019 
    Change-Id: I06767b70a280b2e5780033058cf2c333be5740f9 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6758511 
    Reviewed-by: David Trainor <dtrainor@chromium.org> 
    Commit-Queue: Min Qin <qinmin@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1493653}

```

---

Files:

- M `chrome/browser/download/download_target_determiner.cc`
- M `chrome/browser/download/download_target_determiner_unittest.cc`

---

Hash: [cbd95c7b79a57daf0d850ff4ebc3e9ebf44275ff](http://crrev.com/cbd95c7b79a57daf0d850ff4ebc3e9ebf44275ff)  

Date: Tue Jul 29 17:56:41 2025


---

### aj...@chromium.org (2025-08-30)

Does the CL in comment 6 fix this issue? If so please mark this Fixed.

### sp...@google.com (2025-09-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
exploit mitigation bypass, moderate impact, but mitigated


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### aw...@google.com (2025-11-01)

tomhaas02@, how would you like to be credited for this bug?

### to...@gmail.com (2025-12-01)

Please credit me as Tom Haas.

### ch...@google.com (2025-12-10)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> exploit mitigation bypass, moderate impact, but mitigated

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/431309019)*
