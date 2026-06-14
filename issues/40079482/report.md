# ASSERTION FAILED: static_cast<FileError::ErrorCode>(code) != FileError::ABORT_ERR, Heap-use-after-free in v8::internal::GlobalHandles::Node::Release

| Field | Value |
|-------|-------|
| **Issue ID** | [40079482](https://issues.chromium.org/issues/40079482) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Storage>FileSystem |
| **Reporter** | th...@gmail.com |
| **Assignee** | tz...@chromium.org |
| **Created** | 2014-05-02 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The repro causes a UAF in global-handles set\_state (FileSystem API) with some control over the crash address. Increasing the count var (when the window is being closed), or (string) size of the blob (to be written to the file) will also increase the crash address.

The crash address (therefore) seems to be related to the position in the file when the window is closed (automatically).

**VERSION**  

Chrome Version: 36.0.1933.0 (+) dev, ToT: 261961 (+), 261698 (no crash)  

Operating System: Ubuntu 14.04 x64

**REPRODUCTION CASE**  

(Change count (==10), or the (size of the) blob string ('1') to alter the crash address).

1. Launch the repro script
2. Press "Start"

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab UAF  

Crash State: see added asan trace

## Attachments

- [fsys_close_UAF_repro.html](attachments/fsys_close_UAF_repro.html) (text/html, 930 B)
- [fsys_close_UAF_asan_trace.txt](attachments/fsys_close_UAF_asan_trace.txt) (text/plain, 12.4 KB)

## Timeline

### me...@chromium.org (2014-05-02)

Looks very reproducible. Clusterfuzz is working on the test case.

### cl...@chromium.org (2014-05-02)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=5758508358172672

### cl...@chromium.org (2014-05-02)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5758508358172672

Uploader: meacer@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x62500001ab0b
Crash State:
  - crash stack -
  v8::internal::GlobalHandles::Node::Release
  WebCore::V8FileWriterCallback::~V8FileWriterCallback
  - free stack -
  v8::internal::GlobalHandles::~GlobalHandles
  v8::internal::Isolate::~Isolate
  
Regressed: https://cluster-fuzz.appspot.com//revisions?job=linux_asan_chrome_mp&range=262146:262202

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94LiHQXvjpazZ2TQuycvcL-iB3LqHcGQ4-Tav7zhnhQEkRh0rMEx6bem1VvspOoNi_99wye0_9mPmGCNZ-RmB9538gU1NXTV8AxywtbDAwbvfTAcEpoJY6oMgSM88tG7L7HxCOnOmqBgGEQkRKxrW89ysPixA

Additional requirements: Requires Interaction Gestures



### [Deleted User] (2014-05-06)

[Empty comment from Monorail migration]

### tz...@chromium.org (2014-05-07)

I'm looking into this.

This start failing from http://crrev.com/262184, which enables --child-clean-exit on Asan, as a compile time condition.
Since we don't ship chrome with Asan switch, the particular code-path doesn't hit on the production.

### tz...@chromium.org (2014-05-08)

Reverting Severity to High. I heard we sometimes follow the shutdown sequence on production code.

### bu...@chromium.org (2014-05-08)

The following revision refers to this bug:
  http://src.chromium.org/viewvc/blink?view=rev&rev=173620

------------------------------------------------------------------
r173620 | tzik@chromium.org | 2014-05-08T08:51:53.940710Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/filesystem/FileWriter.cpp?r1=173620&r2=173619&pathrev=173620

[FileAPI] Drop irrelevant ASSERT in FileWriter

The error code can be ABORT_ERR if a operation is aborted by the browser.

BUG=369525

Review URL: https://codereview.chromium.org/267253008
-----------------------------------------------------------------

### in...@chromium.org (2014-05-08)

This was a crash in release build, your fix just removes an assert ?

### ki...@chromium.org (2014-05-08)

#8 - one more patch is coming, r173620 is just a part of fix


### tz...@chromium.org (2014-05-08)

inferno: The assertion failure and UAF are from separate bugs in both blink and chromium.
Another CL is for UAF, which is in CQ now: http://crrev.com/270633009/

### bu...@chromium.org (2014-05-09)

------------------------------------------------------------------
r269345 | tzik@chromium.org | 2014-05-09T17:04:09.414314Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/src/content/child/child_thread.cc?r1=269345&r2=269344&pathrev=269345

[FileAPI] Clean up WebFileSystemImpl before Blink shutdown

WebFileSystemImpl should not outlive V8 instance, since it may have references to V8.
This CL ensures it deleted before Blink shutdown.

BUG=369525

Review URL: https://codereview.chromium.org/270633009
-----------------------------------------------------------------

### bu...@chromium.org (2014-05-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f14efc560a12a513696d6396413b138879dabd7a

commit f14efc560a12a513696d6396413b138879dabd7a
Author: tzik@chromium.org <tzik@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Fri May 09 17:04:09 2014

[FileAPI] Clean up WebFileSystemImpl before Blink shutdown

WebFileSystemImpl should not outlive V8 instance, since it may have references to V8.
This CL ensures it deleted before Blink shutdown.

BUG=369525

Review URL: https://codereview.chromium.org/270633009

git-svn-id: svn://svn.chromium.org/chrome/trunk/src@269345 0039d316-1c4b-4281-b951-d872f2087c98



### tz...@chromium.org (2014-05-10)

Requesting to merge r269345 to M35, which fixes a renderer UAF on renderer shutdown.

### cl...@chromium.org (2014-05-11)

ClusterFuzz has detected this issue as fixed in range 268656:269696.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5758508358172672

Uploader: meacer@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 1
Crash Address: 0x62500001ab0b
Crash State:
  - crash stack -
  v8::internal::GlobalHandles::Node::Release
  WebCore::V8FileWriterCallback::~V8FileWriterCallback
  - free stack -
  v8::internal::GlobalHandles::~GlobalHandles
  v8::internal::Isolate::~Isolate
  
Regressed: https://cluster-fuzz.appspot.com//revisions?job=linux_asan_chrome_mp&range=262146:262202
Fixed: https://cluster-fuzz.appspot.com//revisions?job=linux_asan_chrome_mp&range=268656:269696

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94LiHQXvjpazZ2TQuycvcL-iB3LqHcGQ4-Tav7zhnhQEkRh0rMEx6bem1VvspOoNi_99wye0_9mPmGCNZ-RmB9538gU1NXTV8AxywtbDAwbvfTAcEpoJY6oMgSM88tG7L7HxCOnOmqBgGEQkRKxrW89ysPixA

Additional requirements: Requires Interaction Gestures

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### in...@chromium.org (2014-05-11)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-05-12)

tzik@ - This is unlikely to make M35 as it hasn't landed on dev yet, but we can get this into M35 patch 1.

### ti...@chromium.org (2014-05-12)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-05-12)

[Empty comment from Monorail migration]

### ka...@google.com (2014-05-12)

approved for m35.

### bu...@chromium.org (2014-05-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0ffacf6de1d0d11e3451b86ec990e70c06b40aef

commit 0ffacf6de1d0d11e3451b86ec990e70c06b40aef
Author: tzik@chromium.org <tzik@chromium.org@0039d316-1c4b-4281-b951-d872f2087c98>
Date: Tue May 13 02:42:18 2014

Merge 269345 "[FileAPI] Clean up WebFileSystemImpl before Blink ..."

> [FileAPI] Clean up WebFileSystemImpl before Blink shutdown
> 
> WebFileSystemImpl should not outlive V8 instance, since it may have references to V8.
> This CL ensures it deleted before Blink shutdown.
> 
> BUG=369525
> 
> Review URL: https://codereview.chromium.org/270633009

TBR=tzik@chromium.org

Review URL: https://codereview.chromium.org/286483004

git-svn-id: svn://svn.chromium.org/chrome/branches/1916/src@269974 0039d316-1c4b-4281-b951-d872f2087c98



### bu...@chromium.org (2014-05-13)

------------------------------------------------------------------
r269974 | tzik@chromium.org | 2014-05-13T02:42:18.769038Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/branches/1916/src/content/child/child_thread.cc?r1=269974&r2=269973&pathrev=269974

Merge 269345 "[FileAPI] Clean up WebFileSystemImpl before Blink ..."

> [FileAPI] Clean up WebFileSystemImpl before Blink shutdown
> 
> WebFileSystemImpl should not outlive V8 instance, since it may have references to V8.
> This CL ensures it deleted before Blink shutdown.
> 
> BUG=369525
> 
> Review URL: https://codereview.chromium.org/270633009

TBR=tzik@chromium.org

Review URL: https://codereview.chromium.org/286483004
-----------------------------------------------------------------

### cl...@chromium.org (2014-05-13)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-05-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-05-16)

This bug is a regression and does not impact stable. Removing incorrectly added Release-0-M35 label.

- Your friendly ClusterFuzz

### mb...@chromium.org (2014-05-26)

Thanks for the report! This one qualifies for a $1000 reward.

### ti...@chromium.org (2014-06-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-06-03)

This bug is a regression and does not impact stable. Removing incorrectly added Release-1-M35 label.

- Your friendly ClusterFuzz

### in...@chromium.org (2014-06-04)

Thanks CF for detecting the label mismatch.

### ti...@chromium.org (2014-06-04)

CF wins again!

### ti...@chromium.org (2014-06-09)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-07-22)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-18)

Bulk update: removing view restriction from closed bugs.

### ti...@chromium.org (2014-09-06)

Processing via our e-payment system can take a few weeks, but reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2016-02-02)

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

This issue was migrated from crbug.com/chromium/369525?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079482)*
