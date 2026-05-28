# intent:// can bypass fido:/ URI bock (see: 370482421)

| Field | Value |
|-------|-------|
| **Issue ID** | [401823929](https://issues.chromium.org/issues/401823929) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebAuthentication |
| **Platforms** | Android |
| **Reporter** | Si...@rawet.se |
| **Assignee** | ke...@chromium.org |
| **Created** | 2025-03-09 |
| **Bounty** | $2,000.00 |

## Description

VULNERABILITY DETAILS
It's possbile to bypass the fix for 370482421 by using a intent URI.

VERSION
Chrome Version: 133.0.6943.137 stable
Operating System: Pixel 7 Pro Android 15 March security updates.

REPRODUCTION CASE
See https://issues.chromium.org/issues/370482421 for the original discussion. TL;DR: A website should not be allowed to open FIDO:/ URLs on mobile devices.

The issue is that the original fix was never tested on intent:// URLs. The original fix is a case sensitive check on the intent, it checks for "fido" and not "FIDO".
I have attached a html file whit a POC link that will start FIDO activity when clicked. The file also includes links that are blocked and the console output when clicked.

The fix seams to be fairly straight forward. Use a case insensitive match like what "hasFileSchemeInIntentURI" dose. See attached diff.



CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: [goes here]

## Attachments

- [0da04336.diff](attachments/0da04336.diff) (text/x-diff, 1.2 KB)
- [index.html](attachments/index.html) (text/html, 1.8 KB)

## Timeline

### ph...@chromium.org (2025-03-10)

I can repro this on M133 stable.

Hi kenrb@: Could you please take a look at this bug similar to one you fixed before?

### ch...@google.com (2025-03-10)

Setting milestone because of s2 severity.

### ch...@google.com (2025-03-10)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ke...@chromium.org (2025-03-10)

Thanks for the report. I'm having a look.

### ke...@chromium.org (2025-03-18)

Fixed by <https://chromium-review.googlesource.com/c/chromium/src/+/6367258>.

The GitWatcher bot seems to be having a little vacation.

### ch...@google.com (2025-03-18)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2025-03-19)

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

### ke...@chromium.org (2025-03-19)

1. Which CLs should be backmerged? (Please include Gerrit links.)

<https://chromium-review.googlesource.com/c/chromium/src/+/6367258>

2. Has this fix been verified on Canary to not pose any stability regressions?

It only landed yesterday but it is very low risk.

3. Does this fix pose any potential non-verifiable stability risks?

No.

4. Does this fix pose any known compatibility risks?

No.

5. Does it require manual verification by the test team? If so, please describe required testing.

I've tested the fix locally, but if the test team wants to check also they can use the repro steps from the initial report.

### am...@chromium.org (2025-03-24)

merge approved for <https://crrev.com/c/6367258>, please merge to M135 Beta / branch 7049 at your earliest convenience

### dx...@google.com (2025-03-25)

Project: chromium/src  

Branch: refs/branch-heads/7049  

Author: Ken Buchanan [kenrb@chromium.org](mailto:kenrb@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6392415>

Expand ignore filter for external intent handling

---


Expand for full commit details
```
     
    Many scheme comparisons in ExternalNavigationHandler are case 
    sensitive. This is fine for comparing navigation targets in GURLs, but 
    for `intent://` scheme URLs that specify `scheme=*`, the scheme in the 
    URL parameter can be mixed case and requires a case-insensitive 
    comparison to match. 
     
    This converts several instances of `.equals` to `.equalsIgnoreCase`. 
     
    (cherry picked from commit d412fba0b89c0ba838ae1bef2da2b88e590e18f7) 
     
    Fixed: 401823929 
    Change-Id: Ic9d77d808fb9686ab691f0431918190bf517c3e1 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6367258 
    Commit-Queue: Ken Buchanan <kenrb@chromium.org> 
    Reviewed-by: Michael Thiessen <mthiesse@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1434379} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6392415 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Harry Souders <harrysouders@google.com> 
    Owners-Override: Harry Souders <harrysouders@google.com> 
    Cr-Commit-Position: refs/branch-heads/7049@{#1330} 
    Cr-Branched-From: 2dab7846d0951a552bdc4f350dad497f986e6fed-refs/heads/main@{#1427262}

```

---

Files:

- M `components/external_intents/android/java/src/org/chromium/components/external_intents/ExternalNavigationHandler.java`
- M `components/external_intents/android/javatests/src/org/chromium/components/external_intents/ExternalNavigationHandlerTest.java`

---

Hash: 19ac0182b7df645c2d8f99c5e36350fdc7f05a50  

Date:  Tue Mar 25 18:05:17 2025


---

### sp...@google.com (2025-03-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
report of moderate impact web platform privilege escalation 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-03-26)

Congratulations! We considered this to be on the lower end of moderate impact, but we also appreciate you pointing out where the original fix was insufficient and reporting this to us! 

### pg...@google.com (2025-03-29)

@reporter, how would you like to be credited for this report?

### Si...@rawet.se (2025-03-30)

Hi, thanks for the bounty. You can credit: Simon Rawet.

### ch...@google.com (2025-06-25)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/401823929)*
