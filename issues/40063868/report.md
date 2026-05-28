# Service workers bypass PrivateNetworkAccess for localhost

| Field | Value |
|-------|-------|
| **Issue ID** | [40063868](https://issues.chromium.org/issues/40063868) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>CORS>PrivateNetworkAccess |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | nd...@protonmail.com |
| **Assignee** | ct...@chromium.org |
| **Created** | 2023-04-02 |
| **Bounty** | $1,000.00 |

## Description

**Steps to reproduce the problem:**  

Create a service worker with the contents of:  

"use strict";  

self.addEventListener('fetch', function (event) {  

event.respondWith(fetch(event.request).then(inject));  

});

function inject(response) {  

const headers = new Headers(response.headers);  

return new Response(response.body, { headers: headers });  

}

Register the service worker  

navigator.serviceWorker.register('sw.js');

Send a request to localhost  

const response = await fetch("<http://localhost>", {  

method: "POST",  

body: JSON.stringify({})  

})

**Problem Description:**  

Due to <https://developer.chrome.com/blog/private-network-access-preflight/#how-does-pna-classify-ip-addresses-and-identify-a-private-network>  

The fetch should result in "TypeError: Failed to fetch"

**Additional Comments:**  

I noticed this while testing <https://assets.razerzone.com/dev_portal/REST/html/index.html> not realizing I was abusing a chromium bug :/

\*\*Chrome version: \*\* 111.0.0.0 \*\*Channel: \*\* Stable

**OS:** Windows

## Attachments

- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2023-04-02)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2023-04-02)

Alternatively go to https://random.ndev.tk/sw/ and refresh the page.
Then it should allow the post requests.

### mp...@chromium.org (2023-04-03)

titouan@ PTAL, are these security bugs yet? I also set FoundIn-110 but I'm not sure if this is a defended security boundary all the way back to 100.

[Monorail components: Blink>SecurityFeature>LocalNetworkAccess]

### [Deleted User] (2023-04-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-03)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2023-04-03)

(I am a bot: this is an auto-cc on a security bug)

### [Deleted User] (2023-04-04)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ti...@chromium.org (2023-04-05)

Hi there, and thanks for reaching out!

I don't think this is a bug - rather, it's because PNA is not entirely shipped yet. Your localhost server should be receiving preflights (and if it's not, then we have a bug), but even if the preflights fail, the fetch should be allowed. Preflights are only sent in warning-only mode for now.

### ti...@chromium.org (2023-04-05)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2023-04-05)

From what I can tell there's no preflight.
Also I have chrome://flags/#private-network-access-respect-preflight-results enabled.

While I cant claim this impact stables this should be fixed before deploying the feature fully.

### ph...@chromium.org (2023-04-05)

[Empty comment from Monorail migration]

### ti...@chromium.org (2023-04-06)

Interesting. There are a few toggles at play here:

 - PrivateNetworkAccessSendPreflights: enabled by default
 - PrivateNetworkAccessRespectPreflightResults: disabled by default, enabled by you
 - PrivateNetworkAccessForWorkers: enabled by default
 - PrivateNetworkAccessForWorkersWarningOnly: enabled by default

Because of the last one, even though you turned on RespectPreflightResults, preflights from service workers should only be sent in warning-only mode.

It is concerning that you see no preflight at all. Can you grab a net log and share? Instructions: https://www.chromium.org/for-testers/providing-network-details/

### nd...@protonmail.com (2023-04-06)

Attached net log if there's anything sensitive in it please tell me before this goes public.

### ti...@chromium.org (2023-04-06)

Thanks! In `URL_REQUEST` 459, I see the following:

```
t=3641 [st= 1]          LOCAL_NETWORK_ACCESS_CHECK
                        --> client_address_space = "public"
                        --> resource_address_space = "loopback"
                        --> result = "allowed-by-policy-warn"
```

I would expect to see a policy set to `kWarn` if the service worker was a non-secure context, but I see the following:

```
t=3640 [st= 0]     +URL_REQUEST_START_JOB  [dt=41]
                    --> initiator = "https://random.ndev.tk"
```

So the initiator origin at least https: Given that service workers must be registered same-origin, the document who registered the service worker has an https: origin. I guess it could still be a non-secure context if it was iframed by a non-secure context?

Weird.

### nd...@protonmail.com (2023-04-06)

I don't think service workers normally can be registered on http:
http://localhost would not get blocked by mixed content since its secure anyway.

### ti...@chromium.org (2023-04-06)

You're right, service workers are restricted to https: origins. In fact, they're restricted to secure contexts [1]. A service worker should always be a secure context, then. 

Which, normally, means that they should never get a private network request policy of `kWarn`. But I must be wrong, because that's not what's happening here.

phao@, can you take a look when you have some time?

[1] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/service_worker/service_worker_container.idl;l=34;drc=af69d93ec0d5334cdc03316058660a37116f32b3

### [Deleted User] (2023-04-19)

phao: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-05-01)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ph...@chromium.org (2023-05-05)

No time to look at this yet.  The priority isn't high because PNA for workers would be in warning-only mode anyway.

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### ja...@chromium.org (2023-07-21)

[secondary security shepherd]

Hi phao@, can you clarify https://crbug.com/chromium/1429867#c19? Are you thinking that this isn't a security issue, or are you thinking that fixing this is not needed yet because PNA isn't fully launched yet?

Maybe you can update the Milestone estimate?

### ph...@chromium.org (2023-07-21)

PNA for workers currently only sends warnings on DevTools and doesn't block anything.  There may still be a bug to fix because it should still send preflight requests, but the reporter didn't see any.

I guess this shouldn't be a security bug (at least while PNA for workers is still unlaunched) because even if the preflight requests are sent correctly, chrome won't enforce the response, so the preflight requests can time out or fail but nothing will be blocked.

We don't have a timeline to ship PNA for workers yet.

### ph...@chromium.org (2023-07-24)

[Empty comment from Monorail migration]

### ph...@chromium.org (2023-08-01)

Private network access for worker is an unlaunched feature, so setting Security_Impact-None and removing FoundIn.
We will make sure this is resolved before launching the feature.

### ti...@chromium.org (2023-08-03)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature>CORS>PrivateNetworkAccess]

### ti...@chromium.org (2023-08-03)

[Empty comment from Monorail migration]

[Monorail components: -Blink>SecurityFeature>LocalNetworkAccess]

### ad...@google.com (2023-08-03)

(I am a bot: this is an auto-cc on a security bug)

### is...@google.com (2023-08-03)

This issue was migrated from crbug.com/chromium/1429867?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocking: crbug.com/chromium/1239551]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-26)

Thank you for providing more feedback. Adding the requester to the CC list.

### ph...@google.com (2024-06-04)

Mass re-assigning previous OWP issues to clamy@

### ar...@chromium.org (2024-12-13)

**(secondary security shepherd)**

Hi [clamy@chromium.org](mailto:clamy@chromium.org), I noticed you were assigned, but never commented on the bug. Are you the right owner? What's the status of it?

### cl...@google.com (2024-12-13)

I don't think so. Sending this Chris who has been looking at PNA lately.

### ct...@chromium.org (2025-05-30)

Closing this as resolved:

- We are now confident that the new Local Network Access permission will replace PNA (although Local Network Access is also still only behind a off-by-default flag)
- We have landed enforcement of the Local Network Access permission in service workers (see [Issue 404887282](https://issues.chromium.org/issues/404887282)) which closes this gap in our new implementation

### sp...@google.com (2025-06-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
thank you for report of issue in a feature that did not ship, but helped us make considerations regarding service worker handling in local network access


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-06-04)

Thank you for your efforts and reporting this issue to us.

### nd...@protonmail.com (2025-06-05)

Thanks :)

### ch...@google.com (2025-09-06)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063868)*
