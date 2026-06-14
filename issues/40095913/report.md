# Cross-origin-read attack by using an audio tag to download a cross-origin resource

| Field | Value |
|-------|-------|
| **Issue ID** | [40095913](https://issues.chromium.org/issues/40095913) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Media>Audio, UI>Browser>Downloads |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | li...@chromium.org |
| **Created** | 2019-08-05 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

If a valid resource is used in an audio/video tag, a media player is displayed, which allows one to play/stop the audio/video, change the volume and also download it. A problem exists in that when the user clicks to download the media file, a new request is made, and instead of serving the expected media file, it is possible to do a redirect, which in turn, downloads a cross-origin resource instead of the media file that had been initially loaded into the player.

It looks something like this:

// index.html  

<audio controls>

 <source src="audio.php" type="audio/ogg">
</audio>

// audio.php

<?php
if (isset($\_SERVER["HTTP\_RANGE"])) {
readfile("horse.ogv");
} else {
header("Location: https://victim.lbherrera.me/google/api/secret");
}
?>

This behavior is in itself problematic (<https://crbug.com/chromium/608669>), but under certain conditions could allow an attacker to read cross-origin resources (somewhat similar to <https://crbug.com/chromium/848123>).

The conditions are:

1. The attacker must be able to control the filename/extension of the targeted site.
2. The attacker must be able to insert content into the response of the targeted site.

For [1], many servers allow <http://example.com/secret.json> to be loaded as <http://example.org/secret.json/poc.html>, for example. Another common case is websites that allow people to create usernames containing dots, so it is possible to create a user named "poc.html" (<https://example.com/account/poc.html>).

The attack's idea boils down to inserting a javascript payload "<script>alert('Exfiltration code here')</script>" into an API endpoint that the attacker is able to control the filename/extension and then through the audio/video redirect trick, force the cross-origin resource to be downloaded as HTML. When the user accesses the HTML file that was downloaded, the cross-origin resource will be leaked by the javascript payload that was inserted earlier.

In the PoC, the content of <https://victim.lbherrera.me/google/api/secret> will be read. Also, it is possible to clickjack the user into downloading the file from the audio/video tag (by placing the tag inside an iframe and making it transparent, so that the user is not able to know they are clicking on the three dots and into "Download"). I am out of time right now, but next week, after returning from a trip, I will provide another PoC that demonstrates the attack using clickjacking.

**VERSION**  

Version 76.0.3809.87 (Official Build) stable (64-bit)  

Version 78.0.3874.3 (Official Build) canary (64-bit)

**REPRODUCTION CASE**

1. Access <https://attacker.lbherrera.me/google/index.html>.
2. Click on the three dots and then into "Download".
3. Open the downloaded HTML file.
4. You should see an alert displaying the secret.

**CREDIT INFORMATION**  

Reporter credit: Luan Herrera (@lbherrera\_)

This bug is subject to a 90 day disclosure deadline. After 90 days elapse  

or a patch has been made broadly available (whichever is earlier), the bug  

report will become visible to the public.

## Timeline

### do...@chromium.org (2019-08-05)

Thanks for the report - +downloads and +media folks to investigate.

[Monorail components: Blink>Media>Audio UI>Browser>Downloads]

### sh...@chromium.org (2019-08-06)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-08-06)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ml...@google.com (2019-08-12)

+dalecurtis as it's probably related to the media networking code.

### sh...@chromium.org (2019-08-20)

dtrainor: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dt...@chromium.org (2019-08-20)

[Empty comment from Monorail migration]

### qi...@chromium.org (2019-08-20)

Maybe an easy fix is to ask media element to send the url from the end of the redirect chain to the download and forbid cross origin redirect on the resource request?

### mm...@chromium.org (2019-08-21)

Also CC'ing mlamouri@google.com as the chromium.org accounts says Last visit was > 30 days ago.

### ml...@google.com (2019-08-28)

(thanks mmoroz@, I don't use my chromium.org email and it shouldn't autocomplete)

Assigning liberato@ given that he owns https://crbug.com/chromium/997690 and https://crbug.com/chromium/990849

### li...@chromium.org (2019-08-28)

i'll take a look.

### li...@chromium.org (2019-08-29)

similar to c#7, i think we're just allowing cross-origin redirects on the download, and probably shouldn't be: https://cs.chromium.org/chromium/src/third_party/blink/renderer/modules/media_controls/elements/media_control_download_button_element.cc?rcl=30783628413bbcfd3e186d5be03c536109f1e376&l=82

i'll give it a try.

### li...@chromium.org (2019-08-29)

looks like the only current options are to download or navigate.  DownloadResponseManager::OnReceiveRedirect seems to be the thing that handles this; it just needs to fail the download rather than navigate.

### li...@chromium.org (2019-08-30)

turns out to be more plumbing than i thought.  https://chromium-review.googlesource.com/c/chromium/src/+/1775267

still have to add tests and such.  plus there may be some discussion about exactly the right way to do this with the various owners.

### li...@chromium.org (2019-08-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-10-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a7c8c6b0571d9445cbb17eda0c6467a2a9da39a0

commit a7c8c6b0571d9445cbb17eda0c6467a2a9da39a0
Author: liberato@chromium.org <liberato@chromium.org>
Date: Thu Oct 10 19:30:15 2019

Disallow cross-origin redirects for media downloads.

Cross-origin redirects for downloads aren't allowed, but media
elements didn't notice.  This CL causes them to fail rather than
download or navigate.

It replaces LocalFrameClient::CrossOriginRedirects with the
pre-existing network::mojom::RedirectMode, which includes the
option kError.  We use that to indicate that no cross-origin
redirect should be followed.

Last, this CL partially addresses a TODO in parallel_job_download to
fail redirects, but failing cross-origin redirects.

Change-Id: I10d11962cdc175ae818a0e3f19e4aeaa5a68b959
Bug: 990867
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1779320
Commit-Queue: Frank Liberato <liberato@chromium.org>
Reviewed-by: David Bokan <bokan@chromium.org>
Reviewed-by: Mounir Lamouri <mlamouri@chromium.org>
Reviewed-by: Kinuko Yasuda <kinuko@chromium.org>
Reviewed-by: Min Qin <qinmin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#704762}

[modify] https://crrev.com/a7c8c6b0571d9445cbb17eda0c6467a2a9da39a0/chrome/browser/android/download/download_manager_service.cc
[modify] https://crrev.com/a7c8c6b0571d9445cbb17eda0c6467a2a9da39a0/components/download/content/internal/download_driver_impl.cc
[modify] https://crrev.com/a7c8c6b0571d9445cbb17eda0c6467a2a9da39a0/components/download/internal/common/download_item_impl.cc
[modify] https://crrev.com/a7c8c6b0571d9445cbb17eda0c6467a2a9da39a0/components/download/internal/common/download_response_handler.cc
[modify] https://crrev.com/a7c8c6b0571d9445cbb17eda0c6467a2a9da39a0/components/download/internal/common/parallel_download_job.cc
[modify] https://crrev.com/a7c8c6b0571d9445cbb17eda0c6467a2a9da39a0/components/download/internal/common/resource_downloader.cc
[modify] https://crrev.com/a7c8c6b0571d9445cbb17eda0c6467a2a9da39a0/components/download/public/common/download_response_handler.h
[modify] https://crrev.com/a7c8c6b0571d9445cbb17eda0c6467a2a9da39a0/components/download/public/common/download_url_parameters.cc
[modify] https://crrev.com/a7c8c6b0571d9445cbb17eda0c6467a2a9da39a0/components/download/public/common/download_url_parameters.h
[modify] https://crrev.com/a7c8c6b0571d9445cbb17eda0c6467a2a9da39a0/content/browser/download/download_browsertest.cc
[modify] https://crrev.com/a7c8c6b0571d9445cbb17eda0c6467a2a9da39a0/content/browser/frame_host/render_frame_host_impl.cc
[modify] https://crrev.com/a7c8c6b0571d9445cbb17eda0c6467a2a9da39a0/content/browser/frame_host/render_frame_host_impl.h
[modify] https://crrev.com/a7c8c6b0571d9445cbb17eda0c6467a2a9da39a0/content/common/frame_messages.h
[modify] https://crrev.com/a7c8c6b0571d9445cbb17eda0c6467a2a9da39a0/content/renderer/render_frame_impl.cc
[modify] https://crrev.com/a7c8c6b0571d9445cbb17eda0c6467a2a9da39a0/content/renderer/render_frame_impl.h
[modify] https://crrev.com/a7c8c6b0571d9445cbb17eda0c6467a2a9da39a0/content/renderer/render_frame_impl_browsertest.cc
[modify] https://crrev.com/a7c8c6b0571d9445cbb17eda0c6467a2a9da39a0/content/shell/test_runner/web_frame_test_client.cc
[modify] https://crrev.com/a7c8c6b0571d9445cbb17eda0c6467a2a9da39a0/content/shell/test_runner/web_frame_test_client.h
[modify] https://crrev.com/a7c8c6b0571d9445cbb17eda0c6467a2a9da39a0/content/shell/test_runner/web_frame_test_proxy.cc
[modify] https://crrev.com/a7c8c6b0571d9445cbb17eda0c6467a2a9da39a0/content/shell/test_runner/web_frame_test_proxy.h
[modify] https://crrev.com/a7c8c6b0571d9445cbb17eda0c6467a2a9da39a0/third_party/blink/public/web/DEPS
[modify] https://crrev.com/a7c8c6b0571d9445cbb17eda0c6467a2a9da39a0/third_party/blink/public/web/web_local_frame.h
[modify] https://crrev.com/a7c8c6b0571d9445cbb17eda0c6467a2a9da39a0/third_party/blink/public/web/web_local_frame_client.h
[modify] https://crrev.com/a7c8c6b0571d9445cbb17eda0c6467a2a9da39a0/third_party/blink/renderer/core/exported/local_frame_client_impl.cc
[modify] https://crrev.com/a7c8c6b0571d9445cbb17eda0c6467a2a9da39a0/third_party/blink/renderer/core/exported/local_frame_client_impl.h
[modify] https://crrev.com/a7c8c6b0571d9445cbb17eda0c6467a2a9da39a0/third_party/blink/renderer/core/frame/local_frame_client.h
[modify] https://crrev.com/a7c8c6b0571d9445cbb17eda0c6467a2a9da39a0/third_party/blink/renderer/core/html/html_anchor_element.cc
[modify] https://crrev.com/a7c8c6b0571d9445cbb17eda0c6467a2a9da39a0/third_party/blink/renderer/core/loader/empty_clients.h
[modify] https://crrev.com/a7c8c6b0571d9445cbb17eda0c6467a2a9da39a0/third_party/blink/renderer/modules/media_controls/elements/media_control_download_button_element.cc


### ke...@chromium.org (2019-10-11)

Closing out this security bug since https://crbug.com/chromium/990867#c16 looks like a full resolution. This wouldn't warrant a merge.

### sh...@chromium.org (2019-10-12)

[Empty comment from Monorail migration]

### na...@google.com (2019-10-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-10-15)

Requesting merge to beta M78 because latest trunk commit (704762) appears to be after beta branch point (693954).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-10-15)

This bug requires manual review: We are only 6 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), geohsu@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2019-10-15)

I am rejecting the merge per https://crbug.com/chromium/990867#c17 for M78 and let this go out in M79, 

Adding adetaylor@ as FYI so he is in the loop

### na...@google.com (2019-10-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### pa...@chromium.org (2019-10-18)

Congrats! The Panel decided to reward $500 for this report

### na...@google.com (2019-10-18)

[Empty comment from Monorail migration]

### ad...@google.com (2019-12-05)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-12-06)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-12-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/990867?no_tracker_redirect=1

[Multiple monorail components: Blink>Media>Audio, UI>Browser>Downloads]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095913)*
