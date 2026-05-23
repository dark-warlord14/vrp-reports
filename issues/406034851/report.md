# Insufficient fix for crbug/376625003 (local file read with chrome.devtools)

| Field | Value |
|-------|-------|
| **Issue ID** | [406034851](https://issues.chromium.org/issues/406034851) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 134.0.0.0 |
| **Reporter** | ma...@gmail.com |
| **Assignee** | pf...@google.com |
| **Created** | 2025-03-26 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

(This is more of a theoretical repro because the buggy fix doesn't seem to be merged into anything yet, even canary)
For completeness, I'm re-entering the steps from <https://issues.chromium.org/issues/376625003> :

1. Install the files as a Chrome extension on Mac or Linux
2. Open devtools on the new tab opened by the extension.
3. Edit the /etc/hosts file highlighted in the sources panel, and save the changes.
4. Observe that extension pops up an alert with the new contents of this file.

# Problem Description

The attempted fix [1] for <https://issues.chromium.org/issues/376625003> was to save a local version of URL.prototype.protocol to avoid prototype pollution from a Chrome extension:

```
  const protocolGet = Object.getOwnPropertyDescriptor(URL.prototype, 'protocol')?.get;
  function getProtocol(url: string): string {
    if (!protocolGet) {
      throw new Error('URL.protocol is not available');
    }
    return protocolGet.call(new URL(url));
  }

```

However, an extension can hook Function.prototype.call instead, and still control the output of the getProtocol function. I've attached a standalone-bug.js file that can be run in the console to demonstrate this behavior. getProtocol('file:///etc/hosts') will return 'http:' and therefore canAccessResource() will return true, allowing the extension to read the local file in the same manner as the previous bug.

To fix this, Function.prototype.call should be stored as a constant the same way URL.prototype.protocol was.

Reporter credit: Derin Eryilmaz

1: [https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/5987430/3/front\_end/models/extensions/ExtensionAPI.ts#1140`](https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/5987430/3/front_end/models/extensions/ExtensionAPI.ts#1140%60)

# Additional Comments

j

# Summary

Insufficient fix for [crbug/376625003](https://crbug.com/376625003) (local file read with chrome.devtools)

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- [standalone-bug.js](attachments/standalone-bug.js) (text/javascript, 437 B)
- [background.js](attachments/background.js) (text/javascript, 227 B)
- [manifest.json](attachments/manifest.json) (application/json, 207 B)
- [devtools.html](attachments/devtools.html) (text/html, 36 B)
- [devtools.js](attachments/devtools.js) (text/javascript, 357 B)
- [devtools.js](attachments/devtools.js) (text/javascript, 373 B)
- [standalone-bug.js](attachments/standalone-bug.js) (text/javascript, 453 B)
- [standalone-bug-still-works.js](attachments/standalone-bug-still-works.js) (text/javascript, 784 B)

## Timeline

### ma...@gmail.com (2025-03-26)

Oops, just realize my hook for .call in the original message didn't support multiple arguments, which could technically cause a crash if .call was used in other places in ExtensionAPI.ts. I don't think it's an issue, but in any case, here's updated versions of devtools.js and standalone-bug.js that won't break multi-arg uses of .call elsewhere.

If someone with higher perms than me could replace the files in my original message, that would be highly appreciated.

### ch...@chromium.org (2025-03-27)

Thanks for your report. I can reproduce the behavior described, on Linux in Chrome 134. The incomplete fix to [issue 376625003](https://issues.chromium.org/issues/376625003), <https://chromium-review.googlesource.com/5987430> landed in Chrome 132.

Setting medium severity by the same reasoning that applied to the original bug.

As you suggested, locally confirmed that the bug can be fixed by saving Function.prototype.call, e.g.:

```
diff --git a/front_end/models/extensions/ExtensionAPI.ts b/front_end/models/extensions/ExtensionAPI.ts
index 9529380cf3..2f292fe1fb 100644
--- a/front_end/models/extensions/ExtensionAPI.ts
+++ b/front_end/models/extensions/ExtensionAPI.ts
@@ -1229,6 +1229,7 @@ self.injectedExtensionAPI = function(
   };
 
   const protocolGet = Object.getOwnPropertyDescriptor(URL.prototype, 'protocol')?.get;
+  const functionCall = Object.getOwnPropertyDescriptor(Function.prototype, 'call')?.get;
   function getProtocol(url: string): string {
     if (!protocolGet) {
       throw new Error('URL.protocol is not available');
@@ -1238,6 +1239,8 @@ self.injectedExtensionAPI = function(
 
   function canAccessResource(resource: APIImpl.ResourceData): boolean {
     try {
+      assert(!!functionCall);
+      Function.prototype.call = functionCall;
       return extensionInfo.allowFileAccess || getProtocol(resource.url) !== 'file:';
     } catch {
       return false;

```

danilsomsikov@: Could you please take a look?

### ma...@gmail.com (2025-03-27)

I think that fix still has the same issue because I can use Object.defineProperty to make it so that setting Function.prototype.call does nothing. (File attached for proof). I think functionCall will have to be directly called for it to work.

Edit: I think it might be even better to set Function.prototype.call's writable to false before the extension gets a chance to run.

### da...@google.com (2025-03-27)

Philip, could you please take a look?

### ch...@google.com (2025-03-27)

Setting milestone because of s2 severity.

### ch...@google.com (2025-03-27)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### dx...@google.com (2025-03-31)

Project: devtools/devtools-frontend  

Branch: main  

Author: Philip Pfaffe [pfaffe@chromium.org](mailto:pfaffe@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6401296>

Check file access on the host side of the extension api

---


Expand for full commit details
```
     
    Fixed: 406034851 
    Change-Id: I125bfa572ba9e987569e8524da99de84db83d389 
    Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/6401296 
    Reviewed-by: Danil Somsikov <dsv@chromium.org> 
    Commit-Queue: Philip Pfaffe <pfaffe@chromium.org>

```

---

Files:

- M `front_end/models/extensions/ExtensionAPI.ts`
- M `front_end/models/extensions/ExtensionServer.test.ts`
- M `front_end/models/extensions/ExtensionServer.ts`

---

Hash: cdcca1ad4ef86413b2db3cc5ce546b1a50f91e9e  

Date:  Fri Mar 28 10:17:38 2025


---

### ch...@google.com (2025-03-31)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M135. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [135].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### am...@chromium.org (2025-03-31)

I've updated the `fixed by code changes` as the DevTools -> Chromium roll with the fix so hopefully it won't be rejected as NA again.
The bot was too fast on this one in requesting a merge review, the change didn't make a Canary build just yet.

### ch...@google.com (2025-04-02)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M135. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M136. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [135, 136].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### pf...@google.com (2025-04-02)

1. <https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/6401296>
2. yes
3. I don't think so
4. I don't think so
5. I don't think so

The change already rolled to 136, no need to merge there.

### am...@chromium.org (2025-04-02)

Thanks for fixing this issue. M135 is already shipping to stable. Looking through the change, which is not exactly small and given the amount of direct interaction with devtools required here, I'm going to decline this to backmerge to Stable. Allowing this fix t0 ship in the first Stable release of M136 in three weeks.

### sp...@google.com (2025-04-03)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact user information disclosure 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### ma...@gmail.com (2025-04-03)

Thanks for the reward!

### am...@chromium.org (2025-04-03)

Thanks again for your efforts and reporting this issue to us!

### ch...@google.com (2025-07-08)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of lower impact user information disclosure

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/406034851)*
