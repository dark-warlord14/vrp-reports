# Use-after-poison in blink::TimerBase::runInternal

| Field | Value |
|-------|-------|
| **Issue ID** | [40085361](https://issues.chromium.org/issues/40085361) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Scheduling |
| **Platforms** | Linux |
| **Reporter** | at...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2016-09-10 |
| **Bounty** | $3,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5836363167694848

Fuzzer: attekett_dom_fuzzer
Job Type: linux_asan_chrome_media
Platform Id: linux

Crash Type: Use-after-poison READ 8
Crash Address: 0x7e9026aa55d0
Crash State:
  blink::TimerBase::runInternal
  base::debug::TaskAnnotator::RunTask
  blink::scheduler::TaskQueueManager::ProcessTaskFromWorkQueue
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_media&range=417590:417632

Minimized Testcase (0.09 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv97GFeuOI-uBAQq7cN3WM7uf5zFpltFIgqqOZPvgXq6LO0CChqVSFlEyYwHT9TkzHhJ6yEhVBcGcOlEaG6zp0jsmuvCcmQJ6omVbUb1oKhMETR88lgx14e0-dLZyJaMJ-5UOpdlCBFZ_UMS_Plv4O_20Q5Ui5A?testcase_id=5836363167694848
<meta HTTP-EQUIV="REFRESH" content=0; url=pag
BPt���dm�age.php?site=home&a=0">


Issue filed automatically.

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### sh...@chromium.org (2016-09-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-10)

This issue is a security regression. If you are not able to fix this quickly, please revert the change that introduced it.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-09-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-09-11)

ClusterFuzz has detected this issue as fixed in range 417845:417849.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5836363167694848

Fuzzer: attekett_dom_fuzzer
Job Type: linux_asan_chrome_media
Platform Id: linux

Crash Type: Use-after-poison READ 8
Crash Address: 0x7e9026aa55d0
Crash State:
  blink::TimerBase::runInternal
  base::debug::TaskAnnotator::RunTask
  blink::scheduler::TaskQueueManager::ProcessTaskFromWorkQueue
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_media&range=417590:417632
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_media&range=417845:417849

Minimized Testcase (0.09 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv97GFeuOI-uBAQq7cN3WM7uf5zFpltFIgqqOZPvgXq6LO0CChqVSFlEyYwHT9TkzHhJ6yEhVBcGcOlEaG6zp0jsmuvCcmQJ6omVbUb1oKhMETR88lgx14e0-dLZyJaMJ-5UOpdlCBFZ_UMS_Plv4O_20Q5Ui5A?testcase_id=5836363167694848
<meta HTTP-EQUIV="REFRESH" content=0; url=pag
BPt���dm�age.php?site=home&a=0">


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### wf...@chromium.org (2016-09-12)

attekett can you see if this is reproducible at your end, otherwise I'll just close as a flake.

### at...@gmail.com (2016-09-12)


Almost every machine at my cluster report:

==3834==ERROR: AddressSanitizer: use-after-poison on address 0x7ea64588dd58 at pc 0x7f4cb3e1ff97 bp 0x7ffd79825b70 sp 0x7ffd79825b68                                                                                            READ of size 8 at 0x7ea64588dd58 thread T0 (chrome)
    #0 0x7f4cb3e1ff96 in operator-> ./out/Release/../../third_party/WebKit/Source/wtf/RefPtr.h:68:50                
    #1 0x7f4cb3e1ff96 in WTF::WeakPtrFactory<blink::TimerBase>::revokeAll() ./out/Release/../../third_party/WebKit/Source/wtf/WeakPtr.h:146:0
    #2 0x7f4cb3e202a4 in blink::TimerBase::runInternal() ./out/Release/../../third_party/WebKit/Source/platform/Timer.cpp:124:22
    #3 0x7f4cabd495c7 in Run ./out/Release/../../base/callback.h:56:12                                                    
    #4 0x7f4cabd495c7 in base::debug::TaskAnnotator::RunTask(char const*, base::PendingTask const&) ./out/Release/../../base/debug/task_annotator.cc:54:0

Because of this issue, I haven't tried to reproduce it. I can check it tomorrow, if you guys have problem in reproducing?



### wf...@chromium.org (2016-09-12)

hmm this looks like it could be https://crbug.com/chromium/605718 or https://crbug.com/chromium/638542 maybe I try repro.

### wf...@chromium.org (2016-09-13)

I can't repro on asan win32 build, perhaps this is a race condition. adding some people from the other bugs.

[Monorail components: Blink>Scheduling]

### al...@chromium.org (2016-09-13)

I think this is fixed.  https://codereview.chromium.org/2319053004/ caused a similar error on https://build.chromium.org/p/chromium.webkit/builders/WebKit%20Linux%20ASAN but I moved the revokeAll() after the if (!canFire()) return; in TimerBase::runInternal and the bot was green after re-landing.

I suspect Cluster Fuzz will spot it's fixed by itself soon.

### cl...@chromium.org (2016-09-18)

ClusterFuzz testcase is verified as fixed, closing issue.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2016-09-18)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-23)

And another $3,500 :-)

### aw...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-12-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2016-12-25)

This issue was migrated from crbug.com/chromium/645729?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40085361)*
