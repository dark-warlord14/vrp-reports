# Security: Sandbox escape / automatic code execution via downloads.open

| Field | Value |
|-------|-------|
| **Issue ID** | [40089863](https://issues.chromium.org/issues/40089863) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>Extensions>API |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ju...@gmail.com |
| **Assignee** | sh...@chromium.org |
| **Created** | 2017-12-09 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The chrome.downloads.open API allows automatic code execution due to a race condition when overwriting files. A malicious extension with the "downloads" and "downloads.open" permissions is able to automatically execute code outside any sandboxes without OS or browser warnings.

**VERSION**  

Chrome Version: 63.0.3239.84 + stable  

Operating System: Windows 10 Pro 1709

**REPRODUCTION CASE**  

Attached is an extension that demonstrates the issue. Load it in Chrome, then click on the browser action; calc.exe should open.

The vulnerability arises when two downloads from data: URIs with the same filename and `conflictAction: "overwrite"` are triggered in sequence. The first file is empty (download finishes instantly), the second file contains malicious code and is large enough (download finishes not-quite-so-instantly). When downloads.open is called with the empty file's downloadId after the second file has started downloading but before it finishes, the file executes without any warnings or prompts.

## Attachments

- [testcase.zip](attachments/testcase.zip) (application/octet-stream, 712 B)

## Timeline

### ju...@gmail.com (2017-12-10)

[Comment Deleted]

### ju...@gmail.com (2017-12-10)

There are several contributing issues at play here. Not sure which ones are like that by design and which ones are actual bugs.

- The downloads API allows downloading data: URIs. Firefox WebExtensions in contrast only allow http(s).
- Empty files can be executed without warnings. Zone identifier doesn't get assigned?
- `conflictAction: "overwrite"` allows a file to be executed using a previous download item's ID before it's assigned a zone identifier. This one is definitely a bug.

### ju...@gmail.com (2017-12-10)

It looks like this can be done using http(s) URIs as well, so that's actually not a factor. Timing might be more difficult when the downloaded files are behind a network, though.

### ju...@gmail.com (2017-12-10)

Also, Chrome allows downloads.open to be called from a timer as long as the setTimeout call is done in a click handler. This is probably not intended behavior. Firefox only allows the call to be made directly from a click handler.

### el...@chromium.org (2017-12-10)

[Empty comment from Monorail migration]

[Monorail components: Platform>Extensions>API]

### go...@chromium.org (2017-12-10)

[Empty comment from Monorail migration]

### go...@chromium.org (2017-12-10)

+awhalley@ (Security TPM)

### me...@chromium.org (2017-12-11)

Thanks for the report. I approved the original API given the mitigations (MoTW etc), but I wonder if there is more we can do. 

> - The downloads API allows downloading data: URIs. Firefox WebExtensions in contrast only allow http(s).

I'd support disabling data URL download (not sure how effective of a mitigation this would be, but good for defense in depth).

### el...@chromium.org (2017-12-11)

Re #8: I believe that disabling download of Data URIs would have significant sitecompat impact and likely wouldn't be very helpful unless Blob URIs don't have the same vulnerability for some reason. (The ability to generate files in JavaScript that aren't backed by the server is an important capability to preserve).

### as...@chromium.org (2017-12-11)

Unfortunately, data URL downloads are quite common. They are quite popular for client-side synthesized downloads. Also, they are how Chrome handles "Save image as" from <canvas> elements, and also how resource downloads from the developer console are handled.

I believe what's happening here is purely a race. Once the new download completes (which it does almost instantly for a data URI) and is renamed to its final name, there's a window during which the Windows Attachment Services is invoking known AV products on the host system to scan the file. The MOTW is applied only after the AV products are done looking at the file. If download.open is called for the older overwritten download, then it'd be possible for the new file to be opened prior to the MOTW being applied.

The fact that there was no MOTW for the first download is not relevant.

Calling download.open on the new download is always safe since it doesn't do anything until the final rename is complete and the MOTW is applied.

It is possible for Chrome to know that the older download can no longer be opened by virtue of the new download overwriting it. Chrome could reasonably suppress the open action for older overwritten downloads, thus blocking this vector.


### as...@chromium.org (2017-12-11)

Unfortunately, data URL downloads are quite common. They are quite popular for client-side synthesized downloads. Also, they are how Chrome handles "Save image as" from <canvas> elements, and also how resource downloads from the developer console are handled.

I believe what's happening here is purely a race. Once the new download completes (which it does almost instantly for a data URI) and is renamed to its final name, there's a window during which the Windows Attachment Services is invoking known AV products on the host system to scan the file. The MOTW is applied only after the AV products are done looking at the file. If download.open is called for the older overwritten download, then it'd be possible for the new file to be opened prior to the MOTW being applied.

The fact that there was no MOTW for the first download is not relevant.

Calling download.open on the new download is always safe since it doesn't do anything until the final rename is complete and the MOTW is applied.

It is possible for Chrome to know that the older download can no longer be opened by virtue of the new download overwriting it. Chrome could reasonably suppress the open action for older overwritten downloads, thus blocking this vector.


### as...@chromium.org (2017-12-11)

(Sorry about the duplicate. Crbug is acting up for me today.)

Download.AttachmentServices.Duration measures the total time taken to invoke attachment services. I imagine the MOTW would show up towards the tail end of the invocation unless elawrence@ says otherwise.


### rd...@chromium.org (2017-12-11)

Seeking an owner - asanka@ or benjhayden@, would one of you be able to take this on?

### el...@chromium.org (2017-12-11)

Assigning benjhayden@chromium.org based on ownership of the API. The proposed mitigation "Chrome could reasonably suppress the open action for older overwritten downloads, thus blocking this vector." seems reasonable to me.

I'm setting this to Severity-High based on our triage criteria (Sandbox escape) although the unreliability of the exploit and the precondition of a malicious extension might be an argument to downgrade this to Severity-Medium.

I wasn't able to reproduce this on my z840 running Windows 10 in any version of Chrome; the MOTW-based Attachment Execution Services prompt showed on invocation. This presumably happens either because the machine is too fast or because the security software doesn't hook into the IOfficeAntivirus interface that's invoked by Attachment Execution Services.

On my Lenovo T460S with the default Windows Defender security software, the extension threw an exception "Unchecked runtime.lastError while running downloads.open: Download must be complete" the first time I tried. The second time I tried, it prompted me for a handler for HTA files, then showed the MOTW-based Attachment Execution Services prompt. The third and later tries were successful with no security prompts in both Chrome 63 and Chrome 65.

### ju...@gmail.com (2017-12-11)

> The fact that there was no MOTW for the first download is not relevant.

This is correct. No MOTW on empty files causes another minor problem, though: You could download and open an empty .hta file, then replace it with a malicious download. Now if the user reloads the .hta without closing it (right click -> refresh), the malicious file is executed without warnings.

This is obviously an .hta problem and requires an unlikely user interaction, but could be easily mitigated by making sure empty files get the MOTW as well.

### ju...@gmail.com (2017-12-11)

Re #14: The exploit is very much reliable, the PoC is just a compromise towards readability. On my T460p + Windows Defender it works as-is every time, but reliability can be increased by making the second file considerably larger and slightly increasing the delay before the downloads.open call.

### as...@chromium.org (2017-12-12)

Also +dtrainor for current downloads ownership. David: Do you have someone who can pick this up? The mitigation here would need to be applied in the core downloads layer so that DownloadManagerImpl::OpenDownload() blocks opens for known overwritten downloads after consulting both regular and associated OTR profile data.

For completion, we'd also need to wire in DownloadItem::CanOpenDownload() through its delegate so that the UI / context menus show the "open" action as disabled for overwritten downloads.

Basically we don't want an overwritten DownloadItem to be used to access a new download file.


### dt...@chromium.org (2017-12-12)

shaktisahu@ can you take a look today?

Asanka: Are you suggesting scanning the list of download items when starting a new one and looking for matching file paths?  We would probably need to restore the state in the case that the new download is cancelled.

### as...@chromium.org (2017-12-12)

I was thinking of only allowing "open" for the last download that's in-progress or completed for a given path. This can be determined at the time 'open' is invoked.


### dt...@chromium.org (2017-12-12)

I was a bit worried about a CanOpenDownload() perf hit with the O(N) lookup/comparison, but it looks like it's not called often.  Thanks!

### dt...@chromium.org (2017-12-12)

[Empty comment from Monorail migration]

### dt...@chromium.org (2017-12-12)

@19: We don't need to do this if all downloads are marked as fully completed right?  We only need to limit the opening while the download is in progress or being copied over.  That way we don't have unresponsive items in the UI (thinking about Android downloads home - which doesn't have extensions but I'd rather not have different behavior across platforms).

### as...@chromium.org (2017-12-12)

#22: Correct. This race condition only exists if there's a download in-progress. If all downloads are in terminal states, then there's no race. Only doing the extra work when there's an in-progress download in either the primary or OTR profile is sufficient for this specific issue.

Longer term, it'd be worth considering the UX carefully for the overwrite case. The only real action that can be done with a completed download is to open it, and an overwritten download will always act on a file that doesn't correspond to it. This may be fine if both the new and old download items correspond to the same download URL, but can be quite jarring -- and possibly unsafe -- if not. I'd be inclined to prefer disabled or non-existent download items in the UI over ones that act on unexpected files.

### xi...@chromium.org (2017-12-13)

This exploit mainly bypasses safe browsing check hooked to DownloadTargetDeterminer and QuarantineFile call in content::BaseFile. Is there any other security mechanisms we should be aware of?

QuarantineFile(The platform anti virus hook?) is called after we rename the file on file thread in BaseFile::AnnotateWithSourceInformation. So after the rename and before QuarantineFile called, if the first item is opened, malicious code is executed.

### xi...@chromium.org (2017-12-13)

After QuarantineFile indicate the file is dangerous on file thread, then we delete the file on UI thread in DownloadItemImpl::OnDownloadRenamedToFinalName.

So the gap for malicious code to execute is actually between rename and the file deletion on UI thread.

### as...@chromium.org (2017-12-13)

#24: SafeBrowsing happens prior to the final rename. QuarantineFile happens after the final rename, but before the download is marked as complete. Those two are the only explicitly invoked malware detection mechanisms in Chrome. There are others like on-access scanning which is outside the scope.

Note that QuarantineFile doesn't do a whole lot on non-Windows platforms. On Linux and Mac Chrome annotates the file with origin information, and on Mac this information is used to warn the user upon opening.

As far as general security mechanisms around downloads go, there are many. :-)

#25: On Windows, QuarantineFile will discard the file itself if it was found to be infected or if some registered AV product claims it's bad for any reason. If the file still exists Chrome assumes that the failure is not indicative of a problem with the file (e.g. MOTW application can fail on filesystems that don't support alternate data streams).

It is possible for QuarantineFile to say the file is safe, but still annotate it with a MOTW that causes an additional prompt upon execution. We care very much about this case as well.

Either way, the window of vulnerability begins at the final rename and ends when QuarantineFile is done doing its thing. According to our UMA, this whole process can take multiple seconds on some systems.

Note: Whereever QuarantineFile is mentioned on Windows above, I'm referring to the work done by Windows Attachment Execution services.



In the past we observed that AV treatment of the download file and MOTW application was unreliable if we didn't perform the final rename prior to invoking Attachment Execution Services (hereafter referred to as AES). There's a facility for supplying the target filename so that AVs and AES will use that instead of the on-disk filename, but that didn't seem to work consistently.

It might be worth investigating whether this is still the case. If we can postpone the final rename until after the AES invocation, then that too will squash the vulnerability window.

Though I worry that when it comes to AV, we can never be sure that such cases are handled correctly.

### as...@chromium.org (2017-12-13)

shaktisahu: For completion, can you check whether it's possible for multiple concurrent in-progress downloads to refer to the same path?

This should only be a concern for extensions that can set the conflict action to overwrite for multiple downloads.


### sh...@chromium.org (2017-12-14)

asanka: Regarding #23, do we need to check OTR profile as well? Should it be sufficient to check only the current profile, because in this bug the user uses the downloadId of the old download to open the malicious download. The downloadId won't be available if it is in a different profile? Moreover, in desktop we can have more than two profiles as well.

### as...@chromium.org (2017-12-15)

#28: It depends on whether it's possible to do cross-profile coordination. The OTR suggestion was due to this being more likely in the regular + OTR case than the every-profile case. In the latter the extension needs to be installed in all the associated profiles, while in the former the extension just needs to be allowed in OTR.


### bu...@chromium.org (2017-12-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a8d6ae61d266d8bc44c3dd2d08bda32db701e359

commit a8d6ae61d266d8bc44c3dd2d08bda32db701e359
Author: Shakti Sahu <shaktisahu@chromium.org>
Date: Thu Dec 21 21:33:53 2017

Downloads : Fixed an issue of opening incorrect download file

When one download overwrites another completed download, calling download.open in the old download causes the new download to open, which could be dangerous and undesirable. In this CL, we are trying to avoid this by blocking the opening of the old download.

Bug: 793620
Change-Id: Ic948175756700ad7c08489c3cc347330daedb6f8
Reviewed-on: https://chromium-review.googlesource.com/826477
Reviewed-by: David Trainor <dtrainor@chromium.org>
Reviewed-by: Xing Liu <xingliu@chromium.org>
Reviewed-by: John Abd-El-Malek <jam@chromium.org>
Commit-Queue: Shakti Sahu <shaktisahu@chromium.org>
Cr-Commit-Position: refs/heads/master@{#525810}
[modify] https://crrev.com/a8d6ae61d266d8bc44c3dd2d08bda32db701e359/chrome/browser/download/chrome_download_manager_delegate.cc
[modify] https://crrev.com/a8d6ae61d266d8bc44c3dd2d08bda32db701e359/chrome/browser/download/chrome_download_manager_delegate.h
[modify] https://crrev.com/a8d6ae61d266d8bc44c3dd2d08bda32db701e359/content/browser/download/download_item_impl.cc
[modify] https://crrev.com/a8d6ae61d266d8bc44c3dd2d08bda32db701e359/content/browser/download/download_item_impl_delegate.cc
[modify] https://crrev.com/a8d6ae61d266d8bc44c3dd2d08bda32db701e359/content/browser/download/download_item_impl_delegate.h
[modify] https://crrev.com/a8d6ae61d266d8bc44c3dd2d08bda32db701e359/content/browser/download/download_manager_impl.cc
[modify] https://crrev.com/a8d6ae61d266d8bc44c3dd2d08bda32db701e359/content/browser/download/download_manager_impl.h
[modify] https://crrev.com/a8d6ae61d266d8bc44c3dd2d08bda32db701e359/content/public/browser/download_manager_delegate.cc
[modify] https://crrev.com/a8d6ae61d266d8bc44c3dd2d08bda32db701e359/content/public/browser/download_manager_delegate.h


### sh...@chromium.org (2017-12-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-25)

This bug requires manual review: M64 has already been promoted to the beta branch, so this requires manual review
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), kbleicher@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2017-12-27)

Is this well tested and verified in Canary? Is this a safe merge overall?

### sh...@chromium.org (2017-12-27)

Yes, this is a well isolated change and should be a safe merge overall.

### ab...@google.com (2017-12-28)

Thanks - approving merge for M64. Branch:3282

### aw...@google.com (2018-01-02)

[Empty comment from Monorail migration]

### bu...@chromium.org (2018-01-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4fc004de9e726e36a5110927bfe581bf9ad96b3a

commit 4fc004de9e726e36a5110927bfe581bf9ad96b3a
Author: Shakti Sahu <shaktisahu@chromium.org>
Date: Wed Jan 03 21:47:18 2018

Downloads : Fixed an issue of opening incorrect download file

When one download overwrites another completed download, calling download.open in the old download causes the new download to open, which could be dangerous and undesirable. In this CL, we are trying to avoid this by blocking the opening of the old download.

TBR=shaktisahu@chromium.org

(cherry picked from commit a8d6ae61d266d8bc44c3dd2d08bda32db701e359)

Bug: 793620
Change-Id: Ic948175756700ad7c08489c3cc347330daedb6f8
Reviewed-on: https://chromium-review.googlesource.com/826477
Reviewed-by: David Trainor <dtrainor@chromium.org>
Reviewed-by: Xing Liu <xingliu@chromium.org>
Reviewed-by: John Abd-El-Malek <jam@chromium.org>
Commit-Queue: Shakti Sahu <shaktisahu@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#525810}
Reviewed-on: https://chromium-review.googlesource.com/849195
Reviewed-by: Shakti Sahu <shaktisahu@chromium.org>
Cr-Commit-Position: refs/branch-heads/3282@{#403}
Cr-Branched-From: 5fdc0fab22ce7efd32532ee989b223fa12f8171e-refs/heads/master@{#520840}
[modify] https://crrev.com/4fc004de9e726e36a5110927bfe581bf9ad96b3a/chrome/browser/download/chrome_download_manager_delegate.cc
[modify] https://crrev.com/4fc004de9e726e36a5110927bfe581bf9ad96b3a/chrome/browser/download/chrome_download_manager_delegate.h
[modify] https://crrev.com/4fc004de9e726e36a5110927bfe581bf9ad96b3a/content/browser/download/download_item_impl.cc
[modify] https://crrev.com/4fc004de9e726e36a5110927bfe581bf9ad96b3a/content/browser/download/download_item_impl_delegate.cc
[modify] https://crrev.com/4fc004de9e726e36a5110927bfe581bf9ad96b3a/content/browser/download/download_item_impl_delegate.h
[modify] https://crrev.com/4fc004de9e726e36a5110927bfe581bf9ad96b3a/content/browser/download/download_manager_impl.cc
[modify] https://crrev.com/4fc004de9e726e36a5110927bfe581bf9ad96b3a/content/browser/download/download_manager_impl.h
[modify] https://crrev.com/4fc004de9e726e36a5110927bfe581bf9ad96b3a/content/public/browser/download_manager_delegate.cc
[modify] https://crrev.com/4fc004de9e726e36a5110927bfe581bf9ad96b3a/content/public/browser/download_manager_delegate.h


### aw...@chromium.org (2018-01-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@chromium.org (2018-01-12)

Nice one! The VRP Panel decided to reward $1,000 for this report.  Cheers!

### aw...@chromium.org (2018-01-12)

[Empty comment from Monorail migration]

### aw...@google.com (2018-01-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-01-24)

[Empty comment from Monorail migration]

### aw...@google.com (2018-03-02)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-03-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### aw...@google.com (2018-10-05)

[Empty comment from Monorail migration]

### is...@google.com (2018-10-05)

This issue was migrated from crbug.com/chromium/793620?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40089863)*
