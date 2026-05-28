# Files of extensions with developer tools page are exposed to other extensions

| Field | Value |
|-------|-------|
| **Issue ID** | [428397712](https://issues.chromium.org/issues/428397712) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 138.0.0.0 |
| **Reporter** | gr...@gmail.com |
| **Assignee** | rd...@chromium.org |
| **Created** | 2025-06-29 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

1. Download attached ZIP file and extract its contents.
2. Install each of the three browser extensions that it contains (i.e. "actor", "target-with-devtools" and "target-without-devtools").
3. Open JavaScript console of "actor" extension's service worker.
4. Run the following script (replace "TARGET WITH DEVTOOLS" and "TARGET WITHOUT DEVTOOLS" with the extension ID of the respective extension):

```
async function getFileContent(extensionId, filename) {
    const resp = await fetch(`chrome-extension://${extensionId}/${filename}`);
    return await resp.text();
}

await getFileContent("TARGET WITH DEVTOOLS", "manifest.json")
// '{\n  "manifest_version": 3,\n  "version": "0.1",\n  "name": "Target (with developer tools)",\n  "devtools_page": "devtools.html"\n}\n'

await getFileContent("TARGET WITH DEVTOOLS", "file.txt")
// 'Target extension file (with developer tools panel)\n'

await getFileContent("TARGET WITHOUT DEVTOOLS", "manifest.json")
// Uncaught TypeError: Failed to fetch

await getFileContent("TARGET WITHOUT DEVTOOLS", "file.txt")
// Uncaught TypeError: Failed to fetch

```
# Problem Description

Any extension (despite it not having the "management" permission, or any other permissions) is able to read the contents of files contained within any extension that specifies the "devtools\_page" key in its manifest (despite those files not being declared web-accessible). This allows the actor extension to (a) detect that the target extension is present, and (b) extract any potential secrets contained within the target extension.

# Summary

Files of extensions with developer tools page are exposed to other extensions

# Custom Questions

#### Reporter credit:

Thomas Greiner

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A \

## Attachments

- [chromium-access-ext-files.zip](attachments/chromium-access-ext-files.zip) (application/zip, 2.1 KB)

## Timeline

### dc...@chromium.org (2025-06-30)

This seems rather situational. I'm tempted to give this low, but for now I'll assign it medium. It does seem unintended that having `devtools_page` would make it possible for other chrome extensions to grab resources.

### ch...@google.com (2025-07-01)

Setting milestone because of s2 severity.

### ch...@google.com (2025-07-01)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### da...@google.com (2025-07-08)

Devlin, I believe this is out of out sphere influence. Do you know what makes devtools extension files exposed to the other extensions?

### ch...@google.com (2025-07-23)

rdevlin.cronin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-08-07)

rdevlin.cronin: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-08-22)

rdevlin.cronin: Uh oh! This issue still open and hasn't been updated in the last 44 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-09-06)

rdevlin.cronin: Uh oh! This issue still open and hasn't been updated in the last 59 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2025-09-08)

Project: chromium/src  

Branch:  main  

Author:  Devlin Cronin [rdevlin.cronin@chromium.org](mailto:rdevlin.cronin@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6901326>

[Extensions] Fix devtools accesible resources issue

---


Expand for full commit details
```
     
    There's a bug where resources of devtools extensions are made 
    improperly available. Fix it, and add a regression test. 
     
    Bug: 428397712 
    Change-Id: Ib39ecbe64c571340ec365aa118faca43b643cd8c 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6901326 
    Commit-Queue: Devlin Cronin <rdevlin.cronin@chromium.org> 
    Reviewed-by: Danil Somsikov <dsv@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1512635}

```

---

Files:

- A `chrome/browser/extensions/api/devtools/devtools_apitest.cc`
- M `chrome/browser/extensions/chrome_url_request_util.cc`
- M `chrome/test/BUILD.gn`

---

Hash: [784d50d3c93d2f99ed5268a91fa94496bac7a665](https://chromiumdash.appspot.com/commit/784d50d3c93d2f99ed5268a91fa94496bac7a665)  

Date: Mon Sep 8 20:23:29 2025


---

### rd...@chromium.org (2025-09-17)

This should be fixed with [#comment10](https://issues.chromium.org/issues/428397712#comment10).

### aj...@google.com (2025-09-24)

Setting Low severity as this is a limited leak.

### sp...@google.com (2025-09-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
low impact user information disclosure


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2025-12-25)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/428397712)*
