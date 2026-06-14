# Security: Latest Win10 builds fail to set Mark-of-the-Web on downloaded filenames approaching MAX_PATH

| Field | Value |
|-------|-------|
| **Issue ID** | [40090417](https://issues.chromium.org/issues/40090417) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Windows |
| **Reporter** | gr...@hotmail.com |
| **Assignee** | qi...@chromium.org |
| **Created** | 2018-02-06 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

In <https://crbug.com/chromium/808827#c3> I mentioned that I discovered a mark of the web bypass, I also noticed we can 'bypass' chrome downloaded executable warning by downloading a .EXE instead. I quote bypass because there is still a ping being sent to chrome safe browsing (SBClientDownload.CheckDownloadStats increases in chrome:///histograms) . Though I don't think that's a huge issue as I still run arbitrary code.

VIDEO: <https://www.youtube.com/watch?v=B4jYC0SovDc>

**VERSION**  

Chrome Version: Version 63.0.3239.132 (Official Build) (64-bit)  

Operating System: Windows 10 x64

**REPRODUCTION CASE**

1. unpack attached extensions
2. Wait for a fullscreen window to appear and press MB or any key.

Note: If mark of web bypass doesnt work change the filename in background.js to a larger name or increase the folder depth size. However, if chrome fails to even download the file lessen the length of gilename and/or the depth of folder.

## Attachments

- [poc.zip](attachments/poc.zip) (application/octet-stream, 4.8 KB)
- [Program.cs](attachments/Program.cs) (text/plain, 5.4 KB)

## Timeline

### gr...@hotmail.com (2018-02-07)

Ops, forgot to mention to actually install the extension after step 1! 

Step 1.1: Go to chrome://extensions and click on 'load unpacked extension' and choose any of the files you've unpacked from attached poc.

### el...@chromium.org (2018-02-07)

In your repro case, does the file created get a Mark of the Web at all (e.g. does streams.exe show a Zone.Identifier stream on the file)?

What's the specific build of Windows 10 that you encountered this issue on?

[Monorail components: UI>Browser>Downloads]

### el...@chromium.org (2018-02-07)

Given the behavior of GetEffectiveAuthorityURL, I'd expect GetEffectiveAuthorityURL to result in a marking of "about:internet" which is expected to reliably map to the Internet Zone.

One other point to keep in mind vis-a-vis this repro is that Windows SmartScreen AppRep can remove the MOTW from a file upon execution if the executable is deemed "safe". We'd can test with SmartScreen AppRep disabled to verify that this isn't what's happening.

### gr...@hotmail.com (2018-02-07)

No zone identifier stream is detected. To make sure the streams tool isn't getting confused by the deep folder depth I moved the executable to a normal directory and it did not carry a zone identifier with it.
Tested on Windows 10 Home v1709 OS build 16299.125

### gr...@hotmail.com (2018-02-07)

Might be related to 601538 

### gr...@hotmail.com (2018-02-07)

Can't seem to repro within VM using windows 10 pro, v10.0.10586 build 10586

When i try to open the file from chrome downloads, it doesnt do anything. Pretty sure the flaw still exists as firefox is affected in both environments. Not sure what im missing...

### as...@chromium.org (2018-02-07)

+dtrainor as well.

### in...@chromium.org (2018-02-07)

asanka@, can you please take a look or help find an owner for this.

### el...@chromium.org (2018-02-07)

I haven't been able to reproduce this on Windows 10 1607/14393. In your repro, can you tell us the exact filename that is saved/executed (including all of the path information)?

In the repro, I see the call to GetEffectiveAuthorityURL pass in a source of 

   blob:chrome-extension://fonjaohecbhimmhmapcdpcdffmhpcjbg/daf096ef-d830-445e-ae05-cdd4040e37d9 

and no referer.

Theory: There's a MAX_PATH limitation somewhere. Historically, many Windows APIs would not work properly with a path of over 260 characters. When the Alternate Data Stream is created, its filename is 16 characters longer than the filename to which it is attached [16==strlen(':ZoneIdentifier')]. 

I've previously observed that the Windows team has been making changes to the MOTW file format in the Insider Builds, so it's possible that this is why you're only able to repro on later builds.



### gr...@hotmail.com (2018-02-07)

C:\Users\Abdulrahman\Downloads\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\G\aaaaaaaaaaU.exe

Length=244

It seems it's exactly 260 characters long if you include :ZoneIdentifier hmmm
Is it possible that VMs have simulated NTFS disks and maybe this only works for non vms? Will test on another laptop.

### el...@chromium.org (2018-02-07)

I was able to confirm repro on Windows 10 1709/17074 with a download filename of 246 characters; the file does not get an Alternate Data Stream attached.

When the filename is shorter, the Zone.Identifier stream is present with the expected values:
 
 [ZoneTransfer]
 ZoneId=3
 HostUrl=about:internet



### gr...@hotmail.com (2018-02-07)

Was able to repro on another laptop that has Windows 10 home, v10.0.16299 b16299

### el...@chromium.org (2018-02-07)

Deeply nested file folders are not necessary to reproduce the problem; you can change the code that generates the filename to e.g.

   // MAX_PATH - len(C:\username\downloads) - len(poc.exe) 
   filename:'a'.repeat(260-26-7)+"poc.exe"

...and still reproduce the issue. Note that the POC executable will tend to crash on startup due to a bug in .NET whereby it doesn't like having executable names longer than MAX_PATH.

### gr...@hotmail.com (2018-02-07)

Ah I see. That would be a much better approach since it would execute a tad faster. So it seems like one slight mitigation is guessing OS username length, otherwise you'd have to download&exec multiple files until one executes.

### el...@chromium.org (2018-02-07)

RE #14: Unfortunately, username length isn't a mitigation, because (at least with Canary) Chrome renames the file to a filename short enough to save and long enough to trigger the bug. So exploitation is pretty reliable.

### el...@chromium.org (2018-02-07)

This issue is reproducible even in a normal HTTP(S) download case. 

Firefox is unimpacted because they write the Zone.Identifier directly. IE and Edge are unaffected in the simple case because they truncate the filename early (as they create a temp file in a deeply nested folder); they might be impacted if the filename contains non-ASCII characters.

### gr...@hotmail.com (2018-02-07)

I have a bug filed that is similar to this one with Mozilla. So mark of the web bypass still works on FF. (unless you meant from web version)

Also, how are you determining this is a windows insider problem only? I checked my windows insider app and it appears I am not enrolled in it. The other laptop I used to test and reproduced the problem also isn't an insider. Am I missing something?

### el...@chromium.org (2018-02-07)

Re #17: "Insider" is probably no longer the correct terminology. The regression in the Windows API is only in recent builds, not in older 1607 builds. I've verified that the bug remains in the very latest build, 1709 17083.

I've written a simple test program that shows the IAttachmentExecute Save() API returning S_OK even when it has failed to properly attach the Alternate Data Stream; this bug is not in 1607.

Have you notified secure@microsoft.com of this vulnerability? If not, would you like us to do so and CC you?

### gr...@hotmail.com (2018-02-07)

I haven't and don't mind if you do.

### gr...@hotmail.com (2018-02-07)

[Comment Deleted]

### dt...@chromium.org (2018-02-07)

+qinmin@ does it makes sense to chunk the filename early as well?  Do we want to infer the proper chunk size or should we pick something consistently safe based on MAX_PATH and some buffer?

elawrence@ does this seem like a reasonable fix?

### el...@chromium.org (2018-02-07)

RE #20: I've filed the case with MSRC and your other email address; CRM:0461037482.

RE #21: Does "chunk the filename" mean limiting its length, e.g. as we do inside  download_path_reservation_tracker.cc's ValidatePathAndResolveConflicts() function? Based on what we know now, that seems like a workable fix.

### qi...@chromium.org (2018-02-08)

Yes, truncate the filename is a reasonable fix

### el...@chromium.org (2018-02-08)

[Empty comment from Monorail migration]

### gr...@hotmail.com (2018-02-08)

Wouldn't truncating the filename only fix the web based one? Won't we still be able to create a folder with long length and get same result? Also, is it even expected behavior for the download api to create new folders?

### el...@chromium.org (2018-02-08)

Re #25: Truncation of the fully-qualified filename (including the path) would be expected to fix this issue, but yes, we will absolutely need to test the downloads.downloads() API scenario. 

> is it even expected behavior for the download 
> api to create new folders?

I wondered the same thing. I can see how it might be useful, but it's also a source of risks. FWIW, I tried the simple path traversal attack (with a filename of "/../../file.txt") and it was blocked as an invalid filename.

### el...@chromium.org (2018-02-08)

Microsoft is tracking as MSRC 43569.

### go...@chromium.org (2018-02-13)

M65 Stable promotion is coming VERY soon. Your bug is labelled as Stable ReleaseBlock, pls make sure to land the fix and request a merge  into the release branch ASAP. Thank you.

### bu...@chromium.org (2018-02-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c575e74530267932837e074fa4cdb3df4069d497

commit c575e74530267932837e074fa4cdb3df4069d497
Author: Min Qin <qinmin@chromium.org>
Date: Thu Feb 15 19:15:42 2018

Truncate the length of downloaded file name on windows

During annotation, an extra 16 characters(zone identifier)
are appended to the file name.
That may cause the file path to exceed the 260 character limit.
This CL fixes that problem by truncating the file name when generating
it.

BUG=809759

Change-Id: Ie0baa318ccf5824e3ed4df8cf23386653b6747d7
Reviewed-on: https://chromium-review.googlesource.com/919445
Commit-Queue: Min Qin <qinmin@chromium.org>
Reviewed-by: Eric Lawrence <elawrence@chromium.org>
Reviewed-by: David Trainor <dtrainor@chromium.org>
Cr-Commit-Position: refs/heads/master@{#537093}
[modify] https://crrev.com/c575e74530267932837e074fa4cdb3df4069d497/chrome/browser/download/download_path_reservation_tracker.cc
[modify] https://crrev.com/c575e74530267932837e074fa4cdb3df4069d497/chrome/browser/download/download_path_reservation_tracker_unittest.cc


### aw...@chromium.org (2018-02-16)

qinmin@ - are you expecting to land any more changes or can we mark this as fixed?  Thanks!

### qi...@chromium.org (2018-02-16)

This is fixed now

### sh...@chromium.org (2018-02-17)

[Empty comment from Monorail migration]

### aw...@google.com (2018-02-19)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-02-20)

govind@ - good for 65

### sh...@chromium.org (2018-02-20)

This bug requires manual review: We are only 13 days from stable.
Please contact the milestone owner if you have questions.
Owners: cmasso@(Android), cmasso@(iOS), bhthompson@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2018-02-20)

Approving merge to M65 branch 3325 based on https://crbug.com/chromium/809759#c34. Pls merge ASAP so we can pick it up for this week beta. Thank you.

### bu...@chromium.org (2018-02-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/91b1dca0db211fa76eea4a2da11ef2b59dc8281c

commit 91b1dca0db211fa76eea4a2da11ef2b59dc8281c
Author: Min Qin <qinmin@chromium.org>
Date: Tue Feb 20 18:39:46 2018

Truncate the length of downloaded file name on windows

During annotation, an extra 16 characters(zone identifier)
are appended to the file name.
That may cause the file path to exceed the 260 character limit.
This CL fixes that problem by truncating the file name when generating
it.

BUG=809759
TBR=qinmin@chromium.org

(cherry picked from commit c575e74530267932837e074fa4cdb3df4069d497)

Change-Id: Ie0baa318ccf5824e3ed4df8cf23386653b6747d7
Reviewed-on: https://chromium-review.googlesource.com/919445
Commit-Queue: Min Qin <qinmin@chromium.org>
Reviewed-by: Eric Lawrence <elawrence@chromium.org>
Reviewed-by: David Trainor <dtrainor@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#537093}
Reviewed-on: https://chromium-review.googlesource.com/927041
Reviewed-by: Min Qin <qinmin@chromium.org>
Cr-Commit-Position: refs/branch-heads/3325@{#509}
Cr-Branched-From: bc084a8b5afa3744a74927344e304c02ae54189f-refs/heads/master@{#530369}
[modify] https://crrev.com/91b1dca0db211fa76eea4a2da11ef2b59dc8281c/chrome/browser/download/download_path_reservation_tracker.cc
[modify] https://crrev.com/91b1dca0db211fa76eea4a2da11ef2b59dc8281c/chrome/browser/download/download_path_reservation_tracker_unittest.cc


### el...@chromium.org (2018-02-20)

Verified the fix with the download at https://bayden.com/test/longdl.html. The downloaded file gets a proper MoTW attached with 66.3350.

### aw...@chromium.org (2018-02-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-02-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-02-26)

Congratulations greencardesh@ - the VRP panel decided to award $1,000 for this report - thanks!

### aw...@chromium.org (2018-02-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-03-06)

[Empty comment from Monorail migration]

### el...@chromium.org (2018-04-04)

MSRC reports that they plan to patch this upstream in June 2018 Patch Tuesday.

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-10-11)

[Empty comment from Monorail migration]

### aw...@google.com (2018-11-14)

[Empty comment from Monorail migration]

### is...@google.com (2018-11-14)

This issue was migrated from crbug.com/chromium/809759?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40090417)*
