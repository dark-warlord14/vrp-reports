# Security: UAP in FileReader

| Field | Value |
|-------|-------|
| **Issue ID** | [40055617](https://issues.chromium.org/issues/40055617) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Storage>FileAPI |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | jt...@gmail.com |
| **Assignee** | me...@chromium.org |
| **Created** | 2021-04-21 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**

A FileReader instance is normally referenced in the JavaScript and/or pending\_readers\_/running\_readers\_ of FileReader::ThrottlingController in Blink heap. And there is a way to drop all references to FileReader while it's still loading data, which leads to UAF.

In FileReader::abort,

1. state\_ is set to kDone
2. The abort event is dispatched to user script
3. FileReader::Terminate is called which sets state\_ to kDone again

void FileReader::abort() {  

// ...  

state\_ = kDone; // ======> [1]

base::AutoReset<bool> firing\_events(&still\_firing\_events\_, true);

// Setting error implicitly makes |result| return null.  

error\_ = file\_error::CreateDOMException(FileErrorCode::kAbortErr);

// Unregister the reader.  

ThrottlingController::FinishReaderType final\_step =  

ThrottlingController::RemoveReader(GetExecutionContext(), this);

FireEvent(event\_type\_names::kAbort); // ======> [2]  

FireEvent(event\_type\_names::kLoadend);

// All possible events have fired and we're done, no more pending activity.  

ThrottlingController::FinishReader(GetExecutionContext(), this, final\_step);

// Also synchronously cancel the loader, as script might initiate a new load  

// right after this method returns, in which case an async termination would  

// terminate the wrong loader.  

Terminate(); // ======> [3]  

}

<https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/core/fileapi/file_reader.cc;l=328;drc=eb0355c2458162b6f9cd29ed8810e32814b65e78>

So we can call read methods on the same FileReader in the abort event listener, because state\_ has been set to kDone which could pass the check in FileReader::ReadInternal [4].

void FileReader::ReadInternal(Blob\* blob,  

FileReaderLoader::ReadType type,  

ExceptionState& exception\_state) {  

// If multiple concurrent read methods are called on the same FileReader,  

// InvalidStateError should be thrown when the state is kLoading.  

if (state\_ == kLoading) { // ======> [4]  

exception\_state.ThrowDOMException(  

DOMExceptionCode::kInvalidStateError,  

"The object is already busy reading Blobs.");  

return;  

}  

// ...  

}

<https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/core/fileapi/file_reader.cc;l=277;drc=eb0355c2458162b6f9cd29ed8810e32814b65e78>

In PoC, we firstly create 100 (kMaxOutstandingRequestsPerThread) FileReaders, then call readAsText on the already aborted FileReader (g\_reader). In this case, g\_reader would be pushed in pending\_readers\_. We then schedule a micro task to remove running FileReaders in running\_readers\_ by calling abort method on them so that g\_reader will be executed. After the abort event listener returns, the state\_ of g\_reader will be set to kDone again in FileReader::Terminate, although g\_reader is about to loading data.

There is a listener (progressHandler in PoC) registered for progress event, and in this function we can call readAsText on g\_reader again. At this time, there are two reading requests on g\_reader but only one reference is kept in running\_readers\_ (because running\_readers\_ is a HashSet, not a Queue). When the first reading task is finished, g\_reader would be removed from running\_readers\_.

As to JavaScript world, we can drop the reference to g\_reader by simply set the variable to another value. Now g\_reader could be garbage collected and an UAF would occur when any async callback on the FileReader is called.

This bug should affect the current stable version of Chrome.

**VERSION**  

Chrome Version: 90.0.4430.85 stable

**REPRODUCTION CASE**

1. Setup a HTTPServer  
   
   python -m SimpleHTTPServer 8000
2. Run asan build chrome, and click 'Trigger' button  
   
   ./chrome --js-flags="--expose-gc" <http://localhost:8000/poc.html>

Note that I only tested the poc on custom build Chromium 92.0.4480.2, crash may not happen on other versions because of the uncertainty behavior of GC process, you may adjust the parameter 'n' passed to mygc function in poc to trigger the crash.

**CREDIT INFORMATION**

Rong Jian and Guang Gong of Alpha Lab, Qihoo 360.

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 3.5 KB)
- [asan.log](attachments/asan.log) (text/plain, 17.6 KB)

## Timeline

### [Deleted User] (2021-04-21)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-04-22)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6682182970834944.

### ca...@chromium.org (2021-04-23)

verwaest: Can you help further triage this issue? Neither I nor clusterfuzz could reproduce, but the log seems like a legitimate bug. Thanks.

[Monorail components: Infra>Client>V8]

### ca...@chromium.org (2021-04-23)

[Empty comment from Monorail migration]

### jt...@gmail.com (2021-04-23)

Hi, I download and test an asan-linux-release chromium from [https://storage.googleapis.com/chromium-browser-asan/linux-release/asan-linux-release-873021.zip] ("updated": "2021-04-15T21:24:18.572Z", "cr-git-commit": "8fd8a59cd3dc1b87330cf98280984b36e33bf36d"). The PoC  should works on this version too. Hope this helps to reproduce.

### [Deleted User] (2021-04-23)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-04-23)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-04-23)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ve...@chromium.org (2021-04-29)

jsbell: Can you triage this further? This seems very much outside of my scope.

[Monorail components: -Infra>Client>V8]

### aj...@google.com (2021-04-29)

Adding some OWNERs - please take a look at this security report.

[Monorail components: Blink>Storage>FileAPI]

### js...@chromium.org (2021-04-29)

Passing off to mek@

### aj...@google.com (2021-04-29)

Confirms this repos on Linux asan:-

==1==ERROR: AddressSanitizer: use-after-poison on address 0x7ec026de2ee0 at pc 0x559729ccbaa4 bp 0x7fbc82495ef0 sp 0x7fbc82495ee8
READ of size 8 at 0x7ec026de2ee0 thread T13 (DedicatedWorker)
==1==WARNING: invalid path to external symbolizer!
==1==WARNING: Failed to use and restart external symbolizer!
    #0 0x559729ccbaa3  (/usr/local/google/home/ajgo/chromium/src/out/asan/chrome+0x25805aa3)
    #1 0x559729ccc456  (/usr/local/google/home/ajgo/chromium/src/out/asan/chrome+0x25806456)

I cannot repro on Windows.

### me...@chromium.org (2021-04-29)

I think simply moving the Terminate call to happen before any of the events are dispatched should be enough to fix this.

We should also follow up by fixing the bug that the loadend event should not be dispatched if during the abort event another load started (as per spec), but that bug shouldn't cause any security issues, it's merely a spec compliance thing.

For the general class of FileReaderLoader related UAP bugs, we also have https://crbug.com/chromium/1144264 filed to track making all of this less fragile, as we seem to keep getting bitten by this. Although while that would have fixed the UAP in this specific bug, FileReader would still be in a weird internal state where state_ == kDone but a read is still in progress.

### me...@chromium.org (2021-04-29)

Also note that this is a use-after-poison, not a use-after-free. Not sure if that makes the severity/impact any different, but I imagine a UAP is less exploitable than a UAF since the memory being accessed can't have been reused for anything else yet.

### me...@chromium.org (2021-04-29)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-04-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a74c980df61dd7367ad1b11e6a735be82d2696f0

commit a74c980df61dd7367ad1b11e6a735be82d2696f0
Author: Marijn Kruisselbrink <mek@chromium.org>
Date: Thu Apr 29 19:00:26 2021

FileAPI: Terminate FileReaderLoader before dispatching onabort event.

Otherwise FileReader could end up in an inconsistent state where a load
is still in progress while the state was set to done.

Bug: 1201073
Change-Id: Ib2c833537e1badc57d125568d5d35f53f12582a8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2860442
Reviewed-by: Austin Sullivan <asully@chromium.org>
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Cr-Commit-Position: refs/heads/master@{#877579}

[modify] https://crrev.com/a74c980df61dd7367ad1b11e6a735be82d2696f0/third_party/blink/renderer/core/fileapi/file_reader.cc


### aj...@google.com (2021-04-30)

Thanks - please mark this bug fixed if the above CL resolves the issue - that will kick off the merge process. (security bugs are a bit weird here!)

### as...@chromium.org (2021-04-30)

I imagine mek@ left this open because there's a bit of follow-up work we'd like here, but that has a separate bug (crbug.com/1204139) and the above CL resolves the UAP. This is safe to mark as fixed.

### [Deleted User] (2021-04-30)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-01)

[Empty comment from Monorail migration]

### ad...@google.com (2021-05-03)

mek@ asully@ this is currently marked as impacting only Head (i.e. M92 and later). That seems unlikely to be the case - could you confirm that this affects from M90 onwards?

### as...@chromium.org (2021-05-03)

Yes, this impacts from at least M90 onwards

### ad...@chromium.org (2021-05-03)

Thanks, duly adjusting all the labels.

(Also, I realized I was wrong - this had already been corrected to Security_Impact-Stable, but all the derived downstream labels hadn't been tweaked).

### ad...@chromium.org (2021-05-03)

Approving merge to M90, branch 4430, and M91, branch 4472, unless any problems have shown up in Canary.

For M90 please merge by Thursday EOD PST for next week's stable refresh.

### [Deleted User] (2021-05-03)

This bug requires manual review: M91's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2021-05-04)

[Bulk Edit] Your change has been approved for M91. Please go ahead and merge the CL to branch 4472 (refs/branch-heads/4472) manually asap so that it would be part of tomorrow's Beta release.

### pb...@google.com (2021-05-04)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-05-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/73e026b190a8afa11e3aeb9e00ffd7d387a2d919

commit 73e026b190a8afa11e3aeb9e00ffd7d387a2d919
Author: Marijn Kruisselbrink <mek@chromium.org>
Date: Tue May 04 17:30:06 2021

FileAPI: Terminate FileReaderLoader before dispatching onabort event.

Otherwise FileReader could end up in an inconsistent state where a load
is still in progress while the state was set to done.

(cherry picked from commit a74c980df61dd7367ad1b11e6a735be82d2696f0)

Bug: 1201073
Change-Id: Ib2c833537e1badc57d125568d5d35f53f12582a8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2860442
Reviewed-by: Austin Sullivan <asully@chromium.org>
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#877579}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2871354
Auto-Submit: Marijn Kruisselbrink <mek@chromium.org>
Commit-Queue: Austin Sullivan <asully@chromium.org>
Cr-Commit-Position: refs/branch-heads/4472@{#730}
Cr-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}

[modify] https://crrev.com/73e026b190a8afa11e3aeb9e00ffd7d387a2d919/third_party/blink/renderer/core/fileapi/file_reader.cc


### gi...@appspot.gserviceaccount.com (2021-05-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2ed886f76f3aa42078fc0dba320295a38d795219

commit 2ed886f76f3aa42078fc0dba320295a38d795219
Author: Marijn Kruisselbrink <mek@chromium.org>
Date: Tue May 04 17:54:11 2021

FileAPI: Terminate FileReaderLoader before dispatching onabort event.

Otherwise FileReader could end up in an inconsistent state where a load
is still in progress while the state was set to done.

(cherry picked from commit a74c980df61dd7367ad1b11e6a735be82d2696f0)

Bug: 1201073
Change-Id: Ib2c833537e1badc57d125568d5d35f53f12582a8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2860442
Reviewed-by: Austin Sullivan <asully@chromium.org>
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#877579}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2871355
Commit-Queue: Austin Sullivan <asully@chromium.org>
Auto-Submit: Marijn Kruisselbrink <mek@chromium.org>
Cr-Commit-Position: refs/branch-heads/4430@{#1386}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/2ed886f76f3aa42078fc0dba320295a38d795219/third_party/blink/renderer/core/fileapi/file_reader.cc


### am...@chromium.org (2021-05-07)

[Empty comment from Monorail migration]

### vs...@google.com (2021-05-10)

[Empty comment from Monorail migration]

### am...@google.com (2021-05-10)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-05-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/00f3160d978283173aecd8babfbda9cef6df9ee5

commit 00f3160d978283173aecd8babfbda9cef6df9ee5
Author: Marijn Kruisselbrink <mek@chromium.org>
Date: Wed May 12 08:46:56 2021

FileAPI: Terminate FileReaderLoader before dispatching onabort event.

Otherwise FileReader could end up in an inconsistent state where a load
is still in progress while the state was set to done.

(cherry picked from commit a74c980df61dd7367ad1b11e6a735be82d2696f0)

(cherry picked from commit 2ed886f76f3aa42078fc0dba320295a38d795219)

Bug: 1201073
Change-Id: Ib2c833537e1badc57d125568d5d35f53f12582a8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2860442
Reviewed-by: Austin Sullivan <asully@chromium.org>
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#877579}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2871355
Commit-Queue: Austin Sullivan <asully@chromium.org>
Auto-Submit: Marijn Kruisselbrink <mek@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4430@{#1386}
Cr-Original-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2884067
Owners-Override: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4430_101@{#19}
Cr-Branched-From: 3e9034a21f4b1f6707146b1309e001c3321ab48a-refs/branch-heads/4430@{#1364}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/00f3160d978283173aecd8babfbda9cef6df9ee5/third_party/blink/renderer/core/fileapi/file_reader.cc


### am...@google.com (2021-05-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-05-12)

Congratulations! The VRP Panel has decided to award you $7,500 for this report. Nice work! 

### am...@google.com (2021-05-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### ad...@google.com (2021-06-03)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-04)

[Empty comment from Monorail migration]

### gi...@google.com (2021-06-07)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-06-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c7200e16120643e610f7270a723ddd8bba877533

commit c7200e16120643e610f7270a723ddd8bba877533
Author: Marijn Kruisselbrink <mek@chromium.org>
Date: Mon Jun 07 11:42:10 2021

FileAPI: Terminate FileReaderLoader before dispatching onabort event.

Otherwise FileReader could end up in an inconsistent state where a load
is still in progress while the state was set to done.

(cherry picked from commit a74c980df61dd7367ad1b11e6a735be82d2696f0)

Bug: 1201073
Change-Id: Ib2c833537e1badc57d125568d5d35f53f12582a8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2860442
Reviewed-by: Austin Sullivan <asully@chromium.org>
Commit-Queue: Marijn Kruisselbrink <mek@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#877579}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2883604
Owners-Override: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1660}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/c7200e16120643e610f7270a723ddd8bba877533/third_party/blink/renderer/core/fileapi/file_reader.cc


### vs...@google.com (2021-06-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1201073?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055617)*
