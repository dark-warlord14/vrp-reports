#  iOS Chrome download origin spoof: spoofing downloaded file as it's from any legitimate site via data: URI

| Field | Value |
|-------|-------|
| **Issue ID** | [394997959](https://issues.chromium.org/issues/394997959) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | iOS |
| **Reporter** | pr...@gmail.com |
| **Assignee** | ol...@google.com |
| **Created** | 2025-02-07 |
| **Bounty** | $2,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md

Please see the following link for instructions on filing security bugs: https://www.chromium.org/Home/chromium-security/reporting-security-bugs

Reports may be eligible for reward payments under the Chrome VRP: https://g.co/chrome/vrp

NOTE: Security bugs are normally made public once a fix has been widely deployed.

-------------------------

VULNERABILITY DETAILS
iOS Chrome shows the origin of downloaded files like Desktop Chrome or Android Chrome.

E.g. Following PoC demo on https://malicious-site.com with window.open() will reveal the origin of downloaded file correctly as "https://malicious-site.com"

<script>
function a(){
	window.open('https://google.com/chrome/', 'x');
	setTimeout(function(){
		window.open('/1337.php', 'x');
	}, 3000);
}
</script> 
<center><input type="button" class="button" value="Click here!" onclick="a()"></center>

However, when we abuse data: URI to download the file, utilising it to make it work from a web via loading inside a frame, iOS Chrome thinks its request is from any Top Origin legitimate site allowing to spoof downloaded files as they're from legitimate site.



VERSION
Chrome Version: 134 beta
Operating System: iOS 18.3

REPRODUCTION CASE
Please upload attached html and php files and open ioschromedata.html and click on google.com .

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: [tab, browser, etc.]
Crash State: [see link above: stack trace *with symbols*, registers, exception record]
Client ID (if relevant): [see link above]

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: [goes here]

## Attachments

- [ioschrome_data_spoof.mp4](attachments/ioschrome_data_spoof.mp4) (video/mp4, 2.2 MB)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [1337.php](attachments/1337.php) (application/x-httpd-php, 370 B)
- [ioschromedata.html](attachments/ioschromedata.html) (text/html, 435 B)

## Timeline

### pr...@gmail.com (2025-02-07)

Since the only trusted, legitimate way to confirm the source of files is Chrome's omnibox address bar, this issue allows to spoof any malicious files as if they are from any legitimate site like https://google.com, https://apple.com like https://issues.chromium.org/issues/40055527

### ma...@chromium.org (2025-02-07)

olivierrobin: looks similar to 394997960 but I guess this one is about single downloads and the other 394997960 is about multiple downloads?

### ol...@google.com (2025-02-08)

For this one, the issue is that we rely on WKDownload.originatingFrame.securityOrigin, which is nil for data URL.
We could add a special string if the security origin is not http/https.
@mattm: wdyt?

### ol...@google.com (2025-02-08)

So I tested a few workaround.
One possibility is to use 
WKDownload.originatingFrame.webView.URL if the secureOrigin is nil.
Sadly, tests show that this is very unreliable (it would be worth filing a WebKit bug).
So we don't have a reliable way to get the triggering origin in that case.

Instead, we could show the domain of the downloaded file. I am not sure how good it is security wise.
WDYT?


### th...@chromium.org (2025-02-12)

Thanks for looking into this olivierrobin@. I chatted with some other security folks about this -- from a security perspective, it would probably be ideal if it matched general Desktop URL behavior and showed the initial URL of the site that triggered the download. But if that's not feasible, showing the download URL seems okay. It's also up to Bling UI owners to decide whether your proposed UX seems reasonable for users. Setting severity to Medium.

olivierrobin@ - it sounds like you have been able to reproduce this. Is it reproducible through M132 extended stable? Or is this a regression that was introduced more recently?

### ol...@google.com (2025-02-12)

It has been like this forever.

I am doing a change that will show
- the originating domain
- If it cannot be determined, the download domain (after redirection)
- if it cannot be determined, a placeholder string ("from an unknown source").

This string will only be displayed if it does not match the omnibox domain.

### ap...@google.com (2025-02-13)

Project: chromium/src  

Branch: main  

Author: Olivier Robin <[olivierrobin@google.com](mailto:olivierrobin@google.com)>  

Link:      <https://chromium-review.googlesource.com/6252618>

[IOS] Show the download host if the originating host is not available

---


Expand for full commit details
```
[IOS] Show the download host if the originating host is not available 
 
There are cases where WKDownload.originatingHost.securityOrigin is not 
available (e.g. if the download is initiated from a data frame). 
In that case, display the download origin, after redirection. 
If it is still not available, display a placeholder string to inform 
the user. 
 
Also, observe the WebState to show the URL if the page navigates. 
 
Bug: 394997959, 395232501 
Change-Id: I447e8933676157cc4c345abbb946d13d9e7aff12 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6252618 
Commit-Queue: Olivier Robin <olivierrobin@chromium.org> 
Reviewed-by: Quentin Pubert <qpubert@google.com> 
Reviewed-by: Gauthier Ambard <gambard@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1419891}

```

---

Files:

- M `ios/chrome/app/strings/ios_strings.grd`
- A `ios/chrome/app/strings/ios_strings_grd/IDS_IOS_DOWNLOAD_MANAGER_ORIGIN_HOST_UNKNOWN_LABEL.png.sha1`
- M `ios/chrome/browser/download/ui_bundled/download_manager_consumer.h`
- M `ios/chrome/browser/download/ui_bundled/download_manager_mediator.h`
- M `ios/chrome/browser/download/ui_bundled/download_manager_mediator.mm`
- M `ios/chrome/browser/download/ui_bundled/download_manager_mediator_unittest.mm`
- M `ios/chrome/browser/download/ui_bundled/download_manager_view_controller.mm`
- M `ios/chrome/test/fakes/fake_download_manager_consumer.h`
- M `ios/chrome/test/fakes/fake_download_manager_consumer.mm`
- M `ios/web/download/download_native_task_bridge.h`
- M `ios/web/download/download_native_task_bridge.mm`
- M `ios/web/download/download_native_task_impl.h`
- M `ios/web/download/download_native_task_impl.mm`
- M `ios/web/download/download_task_impl.h`
- M `ios/web/download/download_task_impl.mm`
- M `ios/web/download/download_task_impl_unittest.mm`
- M `ios/web/public/download/download_task.h`
- M `ios/web/public/download/download_task_observer.h`
- M `ios/web/public/test/fakes/fake_download_task.h`
- M `ios/web/public/test/fakes/fake_download_task.mm`

---

Hash: 1c988913e1856a016bb4001056897e6940b77fd7  

Date:  Thu Feb 13 07:32:29 2025


---

### pr...@gmail.com (2025-02-13)

Thanks!

Could you please confirm https://chromium-review.googlesource.com/c/chromium/src/+/6252618 is fixing two different root cause bugs which is following:

1. opaque origin data: download origin spoof

This is original fix which is done few days ago: 

"There are cases where WKDownload.originatingHost.securityOrigin is not
available (e.g. if the download is initiated from a data frame).
In that case, display the download origin, after redirection.
If it is still not available, display a placeholder string to inform
the user."

(for 394997959)

2. First test case (ioschromespoof.html) of https://issues.chromium.org/issues/395232501 : when you trigger download in the same domain, it won't show the origin since it's not necessary as address bar tells you where that downloaded file is from, but because a download bar remains on the same tab after the navigation, this becomes a download origin spoof.

This is second fix which is done few hours ago:

"Also, observe the WebState to show the URL if the page navigates."

(for 395232501)





### ol...@google.com (2025-02-14)

1. Yes, we should show in order
 - the originating host
 - the downloading host
 - "From unknown source"

2. It is only a partial fix as WKDownload has a bug. If the navigation happens too fast, we will get the new domain from WKDownload and there is not much we can do here. I will report that to Apple.

### pr...@gmail.com (2025-02-14)

Thanks, I already reported that second test case (ioschromespoof2.html) which is WKDownload bug as I mentioned in https://issues.chromium.org/issues/395232501#comment8 btw.

### ph...@google.com (2025-02-17)

Setting milestone because of s2 severity.

### ph...@google.com (2025-02-17)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ch...@google.com (2025-03-01)

olivierrobin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-03-02)

olivierrobin: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ol...@google.com (2025-03-03)

There is a blocking bug.
Not sure what flag to add to reflect that.

### ch...@google.com (2025-03-18)

olivierrobin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pr...@gmail.com (2026-04-01)

Hi, these issues were fixed back then by ol...@google.com which is a long time ago. Sorry for not mentioning it here before, I was away due to Dad's operation and treatment afterward

### ya...@google.com (2026-04-09)

From my understanding the root cause of this bug is: crbug.com/501137624. I will mark this bug as `Won't Fix` in the meantime.

### pr...@gmail.com (2026-04-09)

Hi, it seems new report were open to deal with these kind of issues in the future. 

But for these issues: As I stated in comment 9, these issues in this report alone were fixed by olivierrobin@google.com in the commit from comment 8.

So it looks like correct status for this report should've been marked as fixed, a long time ago.

### sp...@google.com (2026-06-08)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline. Security UI Spoofing.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/394997959)*
