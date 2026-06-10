# Fake Downloads and Deceptive Notifications through Browsing History Manipulation.

| Field | Value |
|-------|-------|
| **Issue ID** | [328278718](https://issues.chromium.org/issues/328278718) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Downloads, UI>Browser>Navigation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | st...@gmail.com |
| **Assignee** | qi...@chromium.org |
| **Created** | 2024-03-06 |
| **Bounty** | $5,000.00 |

## Description

# Description

A vulnerability has been identified in the Chromium browser that allows the manipulation of navigation context. This security flaw directly impacts the user experience, as, after clicking on a link from a malicious site, using the browser's back function results in an arbitrary file being downloaded. The concerning aspect is that this download appears to come from a legitimate website, causing confusion and compromising the integrity of information.

The vulnerability manifests as follows:

1. A user accesses a link from a malicious website.
2. When using the back function in the Chromium browser, instead of returning to the previous page, an arbitrary download is initiated automatically.
3. The download deceptively simulates its origin from the current website, leading to confusion by incorrectly indicating that the file originated from the current page rather than the initial website the user navigated from.

# Steps to Reproduce

**Prerequisites: These steps are performed on the Windows operating system.**

**Steps performed by the attacker:**

1. Set up the Ruby interpreter on your system, installing the Sinatra gem.
2. Create a directory named `poc` in a location of your choice.
3. Inside `poc`, create a file named `server.rb` with the following content:

```
require 'sinatra'

set :bind, ARGV[0]
set :port, ARGV[1].to_i

$redirect = false

get '/' do
  $redirect = true
  response.header['Cache-Control'] = 'no-store'
  redirect '/index.html'
end

get '/index.html' do
  response.header['Cache-Control'] = 'no-store'
  if $redirect
    $redirect = false
    File.read('index.html')
  else
    redirect 'data'
  end
end

get '/data' do
  headers 'Cache-Control' => 'no-store',
          'Content-type' => 'application/x-msdownload',
          'Content-Disposition' => 'attachment; filename=Urgent_Chrome_Update.exe'
  File.binread('malware')
end

```

4. In the same directory, create a file named `index.html` with the following content:

```
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Back</title>
</head>
<body>
  <h1>POC SITE</h1>
  <a href="https://google.com">google.com</a>
</body>
</html>

```

5. Place a malicious file in the same directory, named `malware`.
6. Start the server by running `ruby server.rb localhost 80` in a terminal emulator.

**Steps performed by the victim:**

7. Access the address "<http://localhost>" in your web browser.
8. Click on a link that redirects to `google.com`.
9. Subsequently, press the `back` button in the browser. You will observe that instead of returning to the original site, a file download is initiated, seemingly from the current site.
10. Pressing the `back` button again, you will notice how the information bubble indicates that `www.google.com wants to download multiple files`.

Watch the following proof-of-concept video demonstrating how this navigation context manipulation impacts not only file downloads but also system notifications. Deceptively, notification bubbles claim that the download originates from the legitimate website, despite being generated from the attacking site.

**poc.mp4**

# Impact

Exploiting this vulnerability grants the attacker the ability to manipulate the navigation context, resulting in the inadvertent download of a malicious file, such as malware, instead of returning to the original website. This malicious action poses a considerable risk to the security and integrity of the victim's systems, as the user, expecting a return to the website, may be exposed to receiving a file designed to cause harm or compromise the device. Additionally, an additional layer of deception is added, as notification bubbles about the download falsify information, incorrectly indicating that the file originates from the current website rather than the one the user initially navigated from.

The successful exploitation of this vulnerability can have significant consequences, including:

1. Unauthorized file downloads on the user's device.
2. Confusion and loss of trust in the browser's security.
3. Possible execution of phishing attacks by convincing the user that the download comes from a reliable source.

## Attachments

- [poc.mp4](attachments/poc.mp4) (video/mp4, 676.0 KB)
- deleted (application/octet-stream, 0 B)

## Timeline

### ad...@google.com (2024-03-06)

Setting to S4 which means "severity not yet assessed" so it goes to our current security shepherd. That happens to be me. I'll take a look later!

### st...@gmail.com (2024-03-06)

redacted

### ad...@chromium.org (2024-03-06)

Thanks for the report. Reproduced on 122.0.6261.94.

The problem here is step 10 - this "multiple files" warning is showing the wrong origin.

Severity: an address bar spoof with limitations is S2, so that means this probably should be S2 or S3. I'll err on the side of caution and pick S2.

Relevant code seems to be `DownloadRequestLimiter::TabDownloadState::PromptUserForDownload` so assigning based on folks who have recently been thereabouts, in the hopes that they can pass onto the best person to fix this. Specifically, it seems [these lines are probably designed to solve just this sort of problem](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/download/download_request_limiter.cc;drc=f4a00cc248dd2dc8ec8759fb51620d47b5114090;l=595) so sending to qinmin@. Please reassign if necessary!

### cr...@chromium.org (2024-03-06)

Step 9 is also admittedly not ideal, where the download happens without visual indication of where it's from.  Technically the back navigation did the right thing by treating the back URL as a download and not leaving the current page (due to the change in content served), but maybe there's another visual way to indicate where the download came from, like a notification bubble?

(For comparison, if the back navigation had a 204 HTTP response instead of a download or a web page, it would look like clicking the back button did nothing.  We don't really want to show an error page in these download/204 cases, but they're also pretty uncommon unless done intentionally.)

### ad...@google.com (2024-03-06)

(Assuming this affects all Blink platforms - please correct if not so.)

### pe...@google.com (2024-03-07)

Setting milestone because of s2 severity.

### pe...@google.com (2024-03-07)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### st...@gmail.com (2024-03-07)

Dear all, could someone please assist me with the concern I raised in the third comment? Currently, I do not have access to the issue I reported with ID 40071894.

Best regards,
Stan

### ad...@google.com (2024-03-07)

Yep, I re-cc'd you on that one.

### st...@gmail.com (2024-03-07)

Thank you, :)

### al...@chromium.org (2024-03-08)

[Navigation Triage] Adding the "Available" hotlist to move this out of the untriaged state.

### pe...@google.com (2024-03-21)

qinmin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-04-05)

qinmin: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### me...@google.com (2024-06-07)

[Secondary Security Shepherd]

Pinged qinmin@ over email

### qi...@chromium.org (2024-06-07)

I am not able to repro the issue from trunk, however this is reproducible from dev version. Any experiment going on?

### qi...@chromium.org (2024-06-07)

Ok, when running the server locally, the request_initiator from the navigation is empty: https://source.chromium.org/chromium/chromium/src/+/main:content/browser/download/download_manager_impl.cc;l=999

As a result, Chrome is using tab's visible URL in order to show the multiple download warnings.

Not sure if there are anything we need to fix, we can probably silently drop the download in this case, but that may not be ideal either

### na...@chromium.org (2024-09-04)

[Navigation Triage] qinmin@, this is a P1 bug which needs prompt resolution. Please prioritize accordingly working on a solution.

### ap...@google.com (2024-09-06)

Project: chromium/src
Branch: main

commit b76e11c3c3a79c14f89c80042aebd3dbe3b222fb
Author: Min Qin <qinmin@chromium.org>
Date:   Fri Sep 06 19:40:19 2024

    Use URL from download to check if it is allowed when request initiator is empty
    
    Currently Chrome uses request initiator to check if a download should be
    allowed. However, request initiator may be empty for browser initiated
    download. This causes DownloadRequestLimiter to use tab's visible
    URL to determine whether the download should be allowed. However, for
    browser initiated download, the actual URL may be different from the
    visible URL. As a result, this CL fixes the issue by using
    download's URL to determine if download should be allowed.
    
    Bug: 328278718
    Change-Id: I5a5d4a5d09b069ef1bbb8e74ad1630500052236b
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5838818
    Commit-Queue: Min Qin <qinmin@chromium.org>
    Reviewed-by: David Trainor <dtrainor@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1352226}

M       chrome/browser/download/download_request_limiter.cc
M       chrome/browser/download/download_request_limiter.h
M       chrome/browser/download/download_request_limiter_unittest.cc

https://chromium-review.googlesource.com/5838818


### pg...@google.com (2024-10-14)

Hi reporter, how would you like to be credited for this report?

### st...@gmail.com (2024-10-14)

Hi @pg...@google.com,

I would like to receive credit for this report under my nickname "st4nly0n". Additionally, I would like to know if this issue is eligible for a reward.

I look forward to your response.

Best regards,
Stan.

### am...@chromium.org (2024-10-16)

This report will be assessed for a potential reward at by the Chrome VRP panel at a VRP panel session within the next few weeks. Any reward decision will be updated directly on this report at that time. Please see the Chrome VRP FAQ for more information: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/vrp-faq.md>

### pe...@google.com (2024-11-01)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2024-11-01)

1. https://chromium-review.googlesource.com/c/chromium/src/+/5981609
2. Low, there is no conflict.
3. No.
4. Yes, as mentioned in the comment #4, the issue was reproduced on 122.0.6261.94.

### gm...@google.com (2024-11-04)

In M130. Approving for LTS-126

### st...@gmail.com (2024-11-05)

Hi,

In comment #21, I agreed to receive credit for this report; however, it appears as "Anonymous" on https://chromereleases.googleblog.com/2024/. Could anything be done about this?

Kind regards,  
Stan

### ad...@google.com (2024-11-06)

Sorry about that - we'll get it fixed in [the Chrome browser release notes](https://chromereleases.googleblog.com/2024/10/stable-channel-update-for-desktop_15.html) and the [Chrome OS release notes](https://chromereleases.googleblog.com/2024/10/stable-channel-update-for-chromeos_29.html).

### ad...@google.com (2024-11-06)

Release notes updated.

### st...@gmail.com (2024-11-06)

Thank you :)

### ap...@google.com (2024-11-07)

Project: chromium/src  

Branch: refs/branch-heads/6478  

Author: Min Qin <[qinmin@chromium.org](mailto:qinmin@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5981609>

[M126-LTS] Use URL from download to check if it is allowed when request initiator is empty

---


Expand for full commit details
```
[M126-LTS] Use URL from download to check if it is allowed when request initiator is empty 
 
Currently Chrome uses request initiator to check if a download should be 
allowed. However, request initiator may be empty for browser initiated 
download. This causes DownloadRequestLimiter to use tab's visible 
URL to determine whether the download should be allowed. However, for 
browser initiated download, the actual URL may be different from the 
visible URL. As a result, this CL fixes the issue by using 
download's URL to determine if download should be allowed. 
 
(cherry picked from commit b76e11c3c3a79c14f89c80042aebd3dbe3b222fb) 
 
Bug: 328278718 
Change-Id: I5a5d4a5d09b069ef1bbb8e74ad1630500052236b 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5838818 
Commit-Queue: Min Qin <qinmin@chromium.org> 
Reviewed-by: David Trainor <dtrainor@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1352226} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5981609 
Owners-Override: Mohamed Omar <mohamedaomar@google.com> 
Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
Reviewed-by: Mohamed Omar <mohamedaomar@google.com> 
Cr-Commit-Position: refs/branch-heads/6478@{#1992} 
Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

```

---

Files:

- M `chrome/browser/download/download_request_limiter.cc`
- M `chrome/browser/download/download_request_limiter.h`
- M `chrome/browser/download/download_request_limiter_unittest.cc`

---

Hash: dbb2b5298b4b684c1b884a69878fae4192847d75  

Date:  Thu Nov 07 01:30:06 2024


---

### ap...@google.com (2024-11-11)

Project: chromium/src  

Branch: refs/branch-heads/6478\_182  

Author: Min Qin <[qinmin@chromium.org](mailto:qinmin@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6011314>

[CfM-R126] Use URL from download to check if it is allowed when request initiator is empty

---


Expand for full commit details
```
[CfM-R126] Use URL from download to check if it is allowed when request initiator is empty 
 
Currently Chrome uses request initiator to check if a download should be 
allowed. However, request initiator may be empty for browser initiated 
download. This causes DownloadRequestLimiter to use tab's visible 
URL to determine whether the download should be allowed. However, for 
browser initiated download, the actual URL may be different from the 
visible URL. As a result, this CL fixes the issue by using 
download's URL to determine if download should be allowed. 
 
(cherry picked from commit b76e11c3c3a79c14f89c80042aebd3dbe3b222fb) 
 
(cherry picked from commit dbb2b5298b4b684c1b884a69878fae4192847d75) 
 
Bug: 328278718 
Change-Id: I5a5d4a5d09b069ef1bbb8e74ad1630500052236b 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5838818 
Commit-Queue: Min Qin <qinmin@chromium.org> 
Reviewed-by: David Trainor <dtrainor@chromium.org> 
Cr-Original-Original-Commit-Position: refs/heads/main@{#1352226} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5981609 
Owners-Override: Mohamed Omar <mohamedaomar@google.com> 
Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
Reviewed-by: Mohamed Omar <mohamedaomar@google.com> 
Cr-Original-Commit-Position: refs/branch-heads/6478@{#1992} 
Cr-Original-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6011314 
Reviewed-by: Niko Tsirakis <ntsirakis@google.com> 
Owners-Override: Kyle Williams <kdgwill@chromium.org> 
Commit-Queue: Kyle Williams <kdgwill@chromium.org> 
Auto-Submit: Kyle Williams <kdgwill@chromium.org> 
Cr-Commit-Position: refs/branch-heads/6478_182@{#102} 
Cr-Branched-From: 5b5d8292ddf182f8b2096fa665b473b6317906d5-refs/branch-heads/6478@{#1776} 
Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

```

---

Files:

- M `chrome/browser/download/download_request_limiter.cc`
- M `chrome/browser/download/download_request_limiter.h`
- M `chrome/browser/download/download_request_limiter_unittest.cc`

---

Hash: 750269874bf3bcde06518836e32a5049642130b1  

Date:  Mon Nov 11 18:59:38 2024


---

### sp...@google.com (2024-11-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
report of high-quality report of moderate impact security UI spoofing


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-11-15)

Congratulations! Thank you for your efforts and reporting this issue to us -- nice work!

### st...@gmail.com (2024-11-15)

Hello, 

Thank you very much for considering this report as a valid security submission.  

Best regards,  
Stan.

### pe...@google.com (2025-01-21)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/328278718)*
