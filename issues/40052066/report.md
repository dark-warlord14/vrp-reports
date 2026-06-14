# Heap-use-after-free in DatabaseObserver

| Field | Value |
|-------|-------|
| **Issue ID** | [40052066](https://issues.chromium.org/issues/40052066) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | le...@chromium.org |
| **Created** | 2011-12-12 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

use-after-free with worker and sqlite transaction

**VERSION**  

Chrome Version:

Chromium 18.0.970.0 (Developer Build 114015)  

OS Linux  

WebKit 535.13 (@102542)  

JavaScript V8 3.7.12.6

Operating System: linux 64bit

**REPRODUCTION CASE**  

http schema required..

html:

<script>
setTimeout("location.reload()",Math.random()\\*100)
new Worker('empty.js')
</script>

js:

var db = openDatabaseSync("", "", "", 1);  

postMessage("bye");

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: worker (renderer)  

Crash State:

Invalid read of size 4  

at 0x2B5F9FE: WebCore::CrossThreadTask6<WebKit::NewWebCommonWorkerClient\*, WebKit::NewWebCommonWorkerClient\*, WebKit::WebFrame\*, WebKit::WebFrame\*, WTF::String, WTF::String, WTF::String, WTF::String, unsigned long, unsigned long, (anonymous namespace)::AllowDatabaseMainThreadBridge\*, WTF::PassRefPtr<(anonymous namespace)::AllowDatabaseMainThreadBridge> >::performTask(WebCore::ScriptExecutionContext\*) (in /chrome-linux/chromium-browser)

Address 0x13995220 is 0 bytes inside a block of size 64 free'd  

at 0x50425BA: free (vg\_replace\_malloc.c:1081)  

by 0x2B5F8CB: WebCore::DatabaseObserver::canEstablishDatabase(WebCore::ScriptExecutionContext\*, WTF::String const&, WTF::String const&,

## Attachments

- [4864-valgrind.txt](attachments/4864-valgrind.txt) (text/x-c; charset=us-ascii, 21.1 KB)
- [asan-4864.txt](attachments/asan-4864.txt) (text/x-c; charset=us-ascii, 9.9 KB)
- [empty.js](attachments/empty.js) (text/plain; charset=us-ascii, 62 B)
- [4864.html](attachments/4864.html) (text/plain; charset=us-ascii, 96 B)

## Timeline

### in...@chromium.org (2011-12-12)

Yeah i hit this in ClusterFuzz too. we had to reset clusterfuzz becoz of a code change. this is a very recent regression, hopefully, we will hit it soon again. Also, we should also push Miaubiz's testcase.

### in...@chromium.org (2011-12-13)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4413992

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7ff9190da4b0
Crash State:
  - crash stack -
  (anonymous
  (anonymous
  - free stack -
  0x7ffa4ce20add
  0x7ffa4c826e3d
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=113976:113987

Minimized Testcase (0.33 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95iQzMobfcmv3NcpqZlnQmh0vF5NE6ds4CatzdEqrtf0Hb04qNkfNI9wIBvuCF6qsEAuxgz_rOs2eVtlbtVy5LTFqQjtbGhcvdnmuHF7niZTfM8I3krcD4r62d-7puNLo2aMOnJ5HHGGMKpKgHVBcksr0TR1Q

### in...@chromium.org (2011-12-13)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-12-13)

Dave, this might be coming from https://trac.webkit.org/changeset/102473/ based on the regression range https://cluster-fuzz.appspot.com/revisions?range=113976:113987, https://trac.webkit.org/log/?verbose=on&stop_rev=102472&rev=102542&limit=1000

Can you please take a look.

### in...@chromium.org (2011-12-13)

[Empty comment from Monorail migration]

### le...@chromium.org (2011-12-13)

Removed m17. The change was done after m17 branched.

### in...@chromium.org (2011-12-14)

Another repro from ClusterFuzz, has to be run from LayoutTests/fast/workers/storage/interrupt-database.html

### in...@chromium.org (2011-12-14)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4436621

Fuzzer: Inferno_layout_test_fuzzer

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f089d2ca080
Crash State:
  - crash stack -
  WebCore::DatabaseTracker::interruptAllDatabasesForContext
  WebCore::WorkerThread::stop
  - free stack -
  WebCore::SQLTransaction::~SQLTransaction
  WebCore::V8SQLTransaction::derefObject
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=113976:113987

Minimized Testcase (0.53 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv96_x-_2mIN9WjIQl2YFsHrzVvlvg9CPNVs2hhwOBX_ubW7F366raYSBOJ5T0HSFw4e7UWwGZ-9qZPOzhR8cj2TXJv5YK5wx0lX4iTCF_jgbKMShdv4WgAhqSmzLf2NsmANmfcZprd6S2PBO0fxrsVDYaulQ3g
 } catch(e) {}", 134);<meta http-equiv="refresh" content="2"/><script>
{
    document.getElementById("console").innerHTML += message + "<td><defs><defs>";
}

function finishTest()
{
}

function terminateWorker()
{
    worker.terminate();
}

function runTest()
{
    if (window.layoutTestController) {
    }

    worker = new Worker('resources/interrupt-database.js');
    worker.onmessage = function(event) {
        if (event.data == "terminate")
            terminateWorker();
    };
}
</script>
<body onload="runTest()"<feColorMatrix>A0AAA00AAA

### le...@chromium.org (2011-12-15)

cc'ing folks who may review may change or are working on related items.

### [Deleted User] (2011-12-15)

Related: https://bugs.webkit.org/show_bug.cgi?id=74554

### le...@chromium.org (2011-12-15)

Patch up for review in WebKit https://bugs.webkit.org/show_bug.cgi?id=74558


### le...@chromium.org (2011-12-15)

Committed in http://trac.webkit.org/changeset/102894

Rolled into Chromium with r114625

### in...@chromium.org (2011-12-15)

[Empty comment from Monorail migration]

### in...@chromium.org (2011-12-16)

ClusterFuzz confirms testcase in c#0 is fixed by David;s patch. Testcase in c#8 is a different bug, which is now filed as http://code.google.com/p/chromium/issues/detail?id=107873

### sc...@gmail.com (2011-12-21)

@miaubiz: nice regression catch. You caught this before our internal fuzzing efforts and your repro was more minimal that ours :) So a $1000 Chromium Security Reward.

### sc...@gmail.com (2012-02-15)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/107244?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052066)*
