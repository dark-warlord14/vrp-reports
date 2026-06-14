# Security: Android Chrome download files into arbitrary sdcard directory

| Field | Value |
|-------|-------|
| **Issue ID** | [40083415](https://issues.chromium.org/issues/40083415) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Android |
| **Reporter** | dm...@gmail.com |
| **Assignee** | qi...@chromium.org |
| **Created** | 2015-12-17 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Android Chrome can download files into arbitrary sdcard path instead of default download path "/sdcard/Download/". User won't be informed that file will be downloaded into arbitrary sdcard path.

**VERSION**  

Chrome Version: 47.0.2526.83 stable from Google Play  

Operating System: non rooted Android 6.0.1, M8974A-2.0.50.2.28

**REPRODUCTION CASE**  

Server "download.php":

<?
$name = "../chrome/default.txt";
header("Content-Type: application/octet-stream; name=\"readme.txt\"");
header("Content-Disposition: attachment; filename=\"".$name."\"");
echo "hello, world";
?>

Load url like "server/download.php". File will be downloaded into "/sdcard/chrome/" directory instead of "/sdcard/Download/".  

I attach PoC with possible cases of file name (encoded, utf8 encoded).

Video of PoC:  

<https://youtu.be/_CPra2qLqm0> (access only by link)

Looks like DownloadManager (<http://developer.android.com/intl/ru/reference/android/app/DownloadManager.html>) receives subpath argument with traversal path(which must be checked in the application)

## Attachments

- [poc.zip](attachments/poc.zip) (application/zip, 837 B)

## Timeline

### rs...@chromium.org (2015-12-17)

qinmin: Could you please take a look at this issue?

### rs...@chromium.org (2015-12-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-12-18)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-01-08)

qinmin@: Uh oh! This issue is still open and hasn't been updated in the last 21 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### dm...@gmail.com (2016-01-08)

Stable version the same and problem still exists.
I've checked Chrome Beta v 48.0.2564.71, Android 4.4.2, and problem reproduced too.

### dm...@gmail.com (2016-01-18)

Hi, any news? Looks that this is not serious problem?

### cl...@chromium.org (2016-01-29)

qinmin@: Uh oh! This issue is still open and hasn't been updated in the last 42 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ra...@chromium.org (2016-02-18)

qinmin@ - are you able to take a look at this? 

I wonder if this is related to: https://code.google.com/p/chromium/issues/detail?id=586657 ?



### mm...@chromium.org (2016-02-18)

Hrm...  586657 is about FileURLToFilePath, which is solely for decoding local paths for file URLs.  I believe GenerateSafeFileName, GetSuggestedFilename, and GenerateSafeFileName all have protection against this (Checked some of them as a part of that bug, at least their handling of the URL itself).

### as...@chromium.org (2016-02-19)

qinmin: InterceptDownloadResourceThrottle doesn't do any sanitization of the filename extracted from the Content-Disposition header. :-(

### mm...@chromium.org (2016-02-19)

Looks like we pass the raw arguments (Content-Disposition, url) to Java, and then have some Java code that picks the file name:  https://code.google.com/p/chromium/codesearch#chromium/src/chrome/android/java/src/org/chromium/chrome/browser/download/ChromeDownloadDelegate.java&q=requestHttpGetDownload&sq=package:chromium&type=cs&l=231

Instead, it should use net's methods to get the file name, and just pass that to Java instead.

### te...@chromium.org (2016-02-19)

Seems like we could add it here:
https://code.google.com/p/chromium/codesearch#chromium/src/content/browser/android/download_controller_android_impl.cc&l=394

Is that path used both when we use the chrome download stack and the android one?  Do we have to handle those separately?

### as...@chromium.org (2016-02-19)

#12: Chrome downloads stack already has sanitization for filenames.

### qi...@chromium.org (2016-02-19)

So the java side uses URLUtil.guessFileName(String url, String contentDisposition, String mimeType), that function doesn't seem to provide sanitization

### as...@chromium.org (2016-02-19)

StartAndroidDownloadInternal just uses net::HttpContentDisposition to extract the filename from the Content-Disposition header. This method just returns the decoded filename received from the network without any sanitization. It then passes this filename through to DownloadController.newHttpGetDownload(). The filename then passes through the stack as a member of the DownloadInfo structure. I don't see it getting sanitized at any point from there on.

Where is ChromeDownloadDelegate.fileName() called?

### qi...@chromium.org (2016-02-19)

it is called if the content disposition don't have filename specified.

A simple fix is to call net::GetSuggestedFilename() before passing the download to java side, that should give us a non-null file name and it should be sanitized 

### as...@chromium.org (2016-02-19)

#16: Sure, but whether URLUtil.guessFileName() provides sanitization doesn't matter when the attack vector is the Content-Disposition header.

I think in addition to deterministically generating a filename in native code, we should eliminate the guessFileName() call and associated logic on the Java side. That way it's not confusing where the filename is coming from and whether it's sanitized.


### qi...@chromium.org (2016-02-19)

Yes, that's what I am planning to do. 
uploaded https://codereview.chromium.org/1717783002/ to fix the problem

### bu...@chromium.org (2016-02-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/168f723d0f0ce60d92a6307c754181f6d8644583

commit 168f723d0f0ce60d92a6307c754181f6d8644583
Author: qinmin <qinmin@chromium.org>
Date: Thu Feb 25 01:10:38 2016

Fix an issue that download filename from content disposition is not sanitized

The filename from content disposition may not be sanitized.
This change uses net::GetSuggestedFileName() to sanitize the filename
before passing it to java.
Also, there is no need to call URLUtil.guessFileName() since
GetSuggestedFileName() will always return a non-null value.

BUG=570750

Review URL: https://codereview.chromium.org/1717783002

Cr-Commit-Position: refs/heads/master@{#377447}

[modify] https://crrev.com/168f723d0f0ce60d92a6307c754181f6d8644583/chrome/android/java/src/org/chromium/chrome/browser/download/ChromeDownloadDelegate.java
[modify] https://crrev.com/168f723d0f0ce60d92a6307c754181f6d8644583/chrome/android/javatests/src/org/chromium/chrome/browser/download/ChromeDownloadDelegateTest.java
[modify] https://crrev.com/168f723d0f0ce60d92a6307c754181f6d8644583/chrome/browser/android/download/download_manager_service.cc
[modify] https://crrev.com/168f723d0f0ce60d92a6307c754181f6d8644583/content/browser/android/download_controller_android_impl.cc
[modify] https://crrev.com/168f723d0f0ce60d92a6307c754181f6d8644583/content/browser/android/download_controller_android_impl.h
[modify] https://crrev.com/168f723d0f0ce60d92a6307c754181f6d8644583/content/public/browser/android/download_controller_android.h


### qi...@chromium.org (2016-02-25)

[Empty comment from Monorail migration]

### ti...@google.com (2016-02-25)

[Automated comment] Less than 2 weeks to go before stable on M49, manual review required.

### ke...@google.com (2016-03-09)

49 is wrapped, moving to 50.

### cl...@chromium.org (2016-03-10)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

- Your friendly ClusterFuzz

### cl...@chromium.org (2016-03-10)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-04-12)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-04-12)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-04-12)

Thanks for the report. How would you like to be credited when we mention this in Chrome's release notes?

### dm...@gmail.com (2016-04-12)

Hi. Dzmitry Lukyanenko. If possible to add links than I would like to provide my LinkedIn: www.linkedin.com/in/dzima

Thanks:)

### mb...@chromium.org (2016-04-13)

Thanks again for the report! This one qualified for a $500 reward.

### ti...@google.com (2016-04-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/570750?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083415)*
