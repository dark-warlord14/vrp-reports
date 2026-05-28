# out of bound  in function ECPublicKeyFromBytes

| Field | Value |
|-------|-------|
| **Issue ID** | [443196747](https://issues.chromium.org/issues/443196747) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Services (Use Subcomponents)>Sync |
| **Platforms** | Linux, Mac, Windows, iOS, ChromeOS |
| **Chrome Version** | 140.0.0.0 |
| **Reporter** | wx...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2025-09-05 |
| **Bounty** | $5,000.00 |

## Description

# Steps to reproduce the problem

my chromim commit is 6a99accd9be43e397fe4e41571a7e1f5c656ab0d

1. Apply my patch and build Chromium.(This patch only removes the account check that is unrelated to the vulnerability. Since Chromium generally does not have Chrome accounts, I have temporarily disabled it.)
2. out\asan\chrome.exe --no-sandbox <https://accounts.google.com/>
3. Enter the code in the browser’s address bar

```
jaavscript:let buffer = new ArrayBuffer(1);let view = new Uint8Array(buffer);view[0] = 4;chrome.addTrustedSyncEncryptionRecoveryMethod(()=>{console.log("123")},"test", buffer,2);

```

you will see the asan output

# Problem Description

the function <https://source.chromium.org/chromium/chromium/src/+/main:chrome/common/trusted_vault_encryption_keys_extension.mojom;l=28;drc=e3ad182cacc3a02eb6a13091a867815fd17a129c;bpv=0;bpt=1>  

AddTrustedRecoveryMethod(string gaia\_id, array<uint8> public\_key, int32 method\_type\_hint) => ();

This function receives a public\_key sent from the renderer, but it does not perform any length validation. As a result, if the renderer sends malicious data, it will be passed directly to the EC\_POINT\_oct2point function for parsing, which leads to an out-of-bounds read.

Since the renderer parameters are not properly checked here, an exploit prerequisite is either an XSS on accounts.google.com (allowing us to execute arbitrary JavaScript), or a renderer RCE that can send arbitrary IPC messages.

```
let buffer = new ArrayBuffer(1);
let view = new Uint8Array(buffer);
view[0] = 4;
chrome.addTrustedSyncEncryptionRecoveryMethod(()=>{console.log("123")},"test", buffer,2);

```

When this JavaScript snippet is executed on the accounts.google.com page, the buffer with length 1 is passed to EC\_POINT\_oct2point for parsing, resulting in an out-of-bounds read in the browser process.

# Summary

out of bound in function ECPublicKeyFromBytes

# Custom Questions

#### Type of crash:

browser

#### Reporter credit:

raven at KunLun Lab

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 12.6 KB)
- [0001-chrome-test-patch.patch](attachments/0001-chrome-test-patch.patch) (text/x-diff, 3.1 KB)
- [0001-suggest-fix-patch.patch](attachments/0001-suggest-fix-patch.patch) (text/x-diff, 1.0 KB)

## Timeline

### wx...@gmail.com (2025-09-05)

bitset commit: <https://chromium-review.googlesource.com/c/chromium/src/+/2449329>

### wx...@gmail.com (2025-09-05)

sorry, enter this code in the address bar

```
javascript:let buffer = new ArrayBuffer(1);let view = new Uint8Array(buffer);view[0] = 4;chrome.addTrustedSyncEncryptionRecoveryMethod(()=>{console.log("123")},"test", buffer,2);


```

### th...@chromium.org (2025-09-05)

[security shepherd]
I am able to reproduce this on HEAD with the provided patch. IIUC, this is a heap-buffer-overflow in the browser process, though the POC notes: "exploit prerequisite is either an XSS on accounts.google.com (allowing us to execute arbitrary JavaScript), or a renderer RCE that can send arbitrary IPC messages", so I am downgrading this to High severity. Note that the "--no-sandbox" command line flag was not needed for my repro (so that wouldn't make it SecurityImpact-None).

It is unclear to me whether the required patch is valid, i.e. whether it's possible to hit this in a production Chrome scenario without commenting out those lines. If it's not a valid patch, then this would not be a valid security bug.

It is not straightforward to reproduce this not on HEAD since there is a patch required, but there is a bisect listed as https://crrev.com/c/2449329, so I am using that to set the FoundIn as current extended stable (M140).

mastiz@: Could you PTAL at this bug? Please also note if the required patch is not valid (see a couple paragraphs up within this comment).

### ch...@google.com (2025-09-06)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-09-06)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ma...@chromium.org (2025-09-08)

From what I can tell, the attached patch seems unnecessary, the described scenario should be equally reachable without patching Chrome. However, it does influence how many users could be theoretically affected by this report (a few million users at most), in addition to the requirement for XSS on accounts.google.com or a renderer RCE.

### th...@chromium.org (2025-09-08)

Thank you for the response mastiz@. Given that the patch is a valid, then please do prioritize a fix for this bug.

### ma...@chromium.org (2025-09-09)

Ack, SG.

### wx...@gmail.com (2025-09-22)

Hi, any update?

### ma...@chromium.org (2025-09-22)

No updates yet but I plan to look into this soon.

### dx...@google.com (2025-09-26)

Project: chromium/src  

Branch:  main  

Author:  Mikel Astiz [mastiz@chromium.org](mailto:mastiz@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6990129>

[TrustedVault] Fix public import missing size validation

---


Expand for full commit details
```
     
    `SecureBoxPublicKey::CreateByImport()` should have safeguards against 
    input data not matching the expected size, and return null in that case. 
     
    Bug: 443196747 
    Change-Id: I0996dbe383a51b1fd8269fbe429c78f24f283989 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6990129 
    Reviewed-by: Maksim Moskvitin <mmoskvitin@google.com> 
    Commit-Queue: Mikel Astiz <mastiz@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1521442}

```

---

Files:

- M `components/trusted_vault/securebox.cc`
- M `components/trusted_vault/securebox_unittest.cc`

---

Hash: [0e63d7ab62928f5645a42484fbf47cba43b0128f](https://chromiumdash.appspot.com/commit/0e63d7ab62928f5645a42484fbf47cba43b0128f)  

Date: Fri Sep 26 18:49:35 2025


---

### wx...@gmail.com (2025-09-28)

LGTM

### ch...@google.com (2025-09-29)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M140. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M141. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [140, 141].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ts...@google.com (2025-09-30)

Simple fix.  Please merge to M141 (7390) by Friday 3-Oct, and to M142 (7444).

### ma...@chromium.org (2025-09-30)

@ts...@chromium.org can you clarify who is supposed to merge the patch to M141, should I do it?

### ma...@chromium.org (2025-09-30)

Regarding M142, I'm assuming the patch is included in the branch, as it was part of 142.0.7438.0.

### ts...@google.com (2025-09-30)

mastiz, as the author of the patch, you need to perform the merge. This is easiest to accomplish via the web interface to gerrit, using "cherry-pick" from the "..." drop-down menu.

### ma...@chromium.org (2025-09-30)

Sure, np. It just wasn't clear from comment 15, specially considering I didn't request the merge.

Anyway, M141 cherrypick in flight with <https://chromium-review.googlesource.com/c/chromium/src/+/7000268>

### dx...@google.com (2025-09-30)

Project: chromium/src  

Branch:  refs/branch-heads/7390  

Author:  Mikel Astiz [mastiz@chromium.org](mailto:mastiz@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7000268>

[M141][TrustedVault] Fix public import missing size validation

---


Expand for full commit details
```
     
    `SecureBoxPublicKey::CreateByImport()` should have safeguards against 
    input data not matching the expected size, and return null in that case. 
     
    (cherry picked from commit 0e63d7ab62928f5645a42484fbf47cba43b0128f) 
     
    Bug: 443196747 
    Change-Id: I0996dbe383a51b1fd8269fbe429c78f24f283989 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6990129 
    Reviewed-by: Maksim Moskvitin <mmoskvitin@google.com> 
    Commit-Queue: Mikel Astiz <mastiz@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1521442} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7000268 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7390@{#2086} 
    Cr-Branched-From: d481efce5eb300acbb896686676ebd0352a6f1db-refs/heads/main@{#1509326}

```

---

Files:

- M `components/trusted_vault/securebox.cc`
- M `components/trusted_vault/securebox_unittest.cc`

---

Hash: [c7b83421b0c0da04ef18f5455b7ef6d47516c5bb](https://chromiumdash.appspot.com/commit/c7b83421b0c0da04ef18f5455b7ef6d47516c5bb)  

Date: Tue Sep 30 18:35:25 2025


---

### pe...@google.com (2025-09-30)

LTS Milestone M138

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ma...@chromium.org (2025-09-30)

> Was this issue a regression for the milestone it was found in?

No.

> Is this issue related to a change or feature merged after the latest LTS Milestone?

No.

### pe...@google.com (2025-10-02)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2025-10-02)

1. https://chromium-review.googlesource.com/c/chromium/src/+/6998610
2. Low - There was no conflict.,
3. 141
4. Yes, the suspected CL[1] was merged in 2020. So M132 has the issue as well.

[1] https://chromium-review.googlesource.com/c/chromium/src/+/2449329

### pe...@google.com (2025-10-02)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2025-10-02)

1. https://chromium-review.googlesource.com/c/chromium/src/+/6998609
2. Low - There was no conflict.,
3. 141
4. Yes, the suspected CL[1] was merged in 2020. So M138 has the issue as well.

[1] https://chromium-review.googlesource.com/c/chromium/src/+/2449329

### ch...@google.com (2025-10-06)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### sp...@google.com (2025-10-07)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
mildly mitigated memory corruption in the browser process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### wx...@gmail.com (2025-10-08)

I don’t quite understand why this is described as “mildly mitigated memory corruption in the browser process.” Because if we already have an XSS on the account.google.com page or have RCE privileges, we wouldn’t need to trigger it manually. Could you please re-evaluate this?

### wf...@chromium.org (2025-10-17)

re: #29 we did discuss this for a long time in the panel and feel like the $5000 reward is justified here given it was mitigated but in the interests of fairness I will bring it back for evaluation.

### wx...@gmail.com (2025-10-20)

Thank you for your hard work.

### dx...@google.com (2025-10-20)

Project: chromium/src  

Branch:  refs/branch-heads/7204  

Author:  Mikel Astiz [mastiz@chromium.org](mailto:mastiz@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6998609>

[M138-LTS][TrustedVault] Fix public import missing size validation

---


Expand for full commit details
```
     
    `SecureBoxPublicKey::CreateByImport()` should have safeguards against 
    input data not matching the expected size, and return null in that case. 
     
    (cherry picked from commit 0e63d7ab62928f5645a42484fbf47cba43b0128f) 
     
    Bug: 443196747 
    Change-Id: I0996dbe383a51b1fd8269fbe429c78f24f283989 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6990129 
    Reviewed-by: Maksim Moskvitin <mmoskvitin@google.com> 
    Commit-Queue: Mikel Astiz <mastiz@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1521442} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6998609 
    Reviewed-by: Mikel Astiz <mastiz@chromium.org> 
    Reviewed-by: Artem Sumaneev <asumaneev@google.com> 
    Owners-Override: Artem Sumaneev <asumaneev@google.com> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Cr-Commit-Position: refs/branch-heads/7204@{#3434} 
    Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```

---

Files:

- M `components/trusted_vault/securebox.cc`
- M `components/trusted_vault/securebox_unittest.cc`

---

Hash: [c05f6191249c20960e677f17526322a88d647d55](https://chromiumdash.appspot.com/commit/c05f6191249c20960e677f17526322a88d647d55)  

Date: Mon Oct 20 03:57:40 2025


---

### wf...@chromium.org (2025-10-23)

Hello, the panel looked very closely again at this reward amount and agreed that the current $5000 reward was appropriate here.

### wx...@gmail.com (2025-10-27)

Ok.Thank you for your hard work again.

### ch...@google.com (2026-01-06)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/443196747)*
