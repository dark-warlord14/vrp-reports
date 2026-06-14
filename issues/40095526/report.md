# Security: Navigating to "chrome://" URLs on Android 

| Field | Value |
|-------|-------|
| **Issue ID** | [40095526](https://issues.chromium.org/issues/40095526) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Navigation |
| **Platforms** | Android |
| **Reporter** | ch...@gmail.com |
| **Assignee** | qi...@chromium.org |
| **Created** | 2019-06-28 |
| **Bounty** | $500.00 |

## Description

**VERSION**  

Chrome Version: 77.0.3836.3 canary  

Operating System: Android

Similar to <https://crbug.com/chromium/528505>

**REPRODUCTION CASE**

1. Go to  
   
   <https://shhnjk.azurewebsites.net/download_redirector.php?url=chrome://history>
2. Observe

## Timeline

### jd...@chromium.org (2019-06-28)

ahemery@: can you take a look at this? It's manifesting in Android, but based on https://crbug.com/979443, may have a underlying navigation issue. Feel free to pass it to someone you think would be better suited. Thanks!

[Monorail components: UI>Browser>Navigation]

### ah...@chromium.org (2019-07-01)

Hey Joe! will take a look, could you cc me on the other bug as well? I don't have access.

### es...@chromium.org (2019-08-21)

I cc'ed you on the other bug, though I'm not sure if it's related.

chromium.khalil, could you please include the php script that you are using to serve this POC?

For posterity, this is the contents of the HTML:

<a href="/location.php?url=chrome://history" download>Download</a>
<script>
document.querySelector("a").click();
</script>
<a href="javascript:alert('I am '+self.origin)">WhoAmI?</a>

### es...@chromium.org (2019-08-21)

ccing some Android people as well since this seems Android-specific

### te...@chromium.org (2019-08-22)

This seems to depend on the download happening (if I am able to block automatic downloads for this site then it no longer works).  Adding some downloads folk.

### ch...@gmail.com (2019-09-12)

Still able repro on M79.0.3909.0 (This can repro on Desktop too). 

(This CL https://chromium-review.googlesource.com/c/chromium/src/+/1768825 didn't fix this) .

### qi...@chromium.org (2019-09-12)

Maybe because the final navigation didn't check CanRequestURL(). 

### qi...@chromium.org (2019-09-12)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-09-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/89e3e7a034ae69f47030f68c14db2c5fa3035884

commit 89e3e7a034ae69f47030f68c14db2c5fa3035884
Author: Min Qin <qinmin@chromium.org>
Date: Thu Sep 12 23:44:32 2019

Check whether a redirected URL can be requeted first

This CL reorders some checks in
DownloadResponseHandler::OnReceiveRedirect.
The new ordering is:
1. Whether redirect URL can be requested.
2. Cross origin redirect
3. partial request.

BUG=979441

Change-Id: Ia9c3f0ecb481d2933174ab3fd17df4116ba6db3a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1801327
Reviewed-by: Xing Liu <xingliu@chromium.org>
Commit-Queue: Min Qin <qinmin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#696220}

[modify] https://crrev.com/89e3e7a034ae69f47030f68c14db2c5fa3035884/components/download/internal/common/download_response_handler.cc


### qi...@chromium.org (2019-09-12)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-13)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-16)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-09-30)

Congrats! The Panel decided to reward $500 for this report :)  

### na...@google.com (2019-09-30)

[Empty comment from Monorail migration]

### ad...@google.com (2019-12-05)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-12-06)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-12-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-12-20)

This issue was migrated from crbug.com/chromium/979441?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095526)*
