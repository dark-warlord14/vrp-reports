# Use-after-free in blink::WebSharedWorkerImpl::stopWorkerThread

| Field | Value |
|-------|-------|
| **Issue ID** | [40080120](https://issues.chromium.org/issues/40080120) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Workers |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ho...@chromium.org |
| **Created** | 2014-07-28 |
| **Bounty** | $1,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4713408970620928

Fuzzer: Therealholden_worker
Job Type: Mac_asan_chrome

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x59b26f7c
Crash State:
  - crash stack -
  content::EmbeddedSharedWorkerStub::OnMessageReceived
  content::MessageRouter::RouteMessage
  - free stack -
  blink::WebSharedWorkerImpl::terminateWorkerContext
  content::EmbeddedSharedWorkerStub::OnMessageReceived
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv960Z9eT9m9H8DQGFKEPK2xpFC74ID7hBzK0RAl4gpmLKk740Zj2ucIuFPzYlEY1VxkiWDCOMbv--v9xeqWJynr3heax7BwZTApZK9emFdOuUvpGZhRCuVgVHeYLESrUWdZPFbVEx5Ciw-c3NaeHZ6ReIYzNEw


Filer: inferno

## Attachments

- [heavy_file_io.html](attachments/heavy_file_io.html) (text/html, 1013 B)

## Timeline

### in...@chromium.org (2014-07-28)

Looks like regression from http://src.chromium.org/viewvc/blink?view=revision&revision=179011

### cl...@chromium.org (2014-07-29)

[Empty comment from Monorail migration]

### ko...@chromium.org (2014-07-29)

[Empty comment from Monorail migration]

### ko...@chromium.org (2014-07-29)

Looking at https://cluster-fuzz.appspot.com/testcase?key=6604830963400704 which seems to be a same repro case but on Linux.

Hmm, I can't make it to crash, but reloading the page does make content_shell unresposnive.

### ko...@chromium.org (2014-07-29)

Looks like the repro case makes content_shell unresponsive even with the CL reverted. I'll revert the CL for now, and first try to fix freeze from the repro case.

### ko...@chromium.org (2014-07-29)

Revert CL: https://codereview.chromium.org/424923002/

### in...@chromium.org (2014-07-29)

Sorry testcase was one-time crasher in both cases. But looks like delete this in your cl triggered this, so good to revert it.

### ko...@chromium.org (2014-07-29)

Landed the revert CL, but the content_shell still becomes unresponsive.

Hmm. Looks like the worker implementation is spamming browser messages???
I don't have enough expertise to work on this bug, so assigning to worker expert horo-san.

horo: Would you take a look?

### ho...@chromium.org (2014-07-30)

I think it is not related to Workers.
The heavy file operations can make the browser process unresponsive without using Workers.



### ko...@chromium.org (2014-07-30)

+tzik for DOS issue.

### tz...@chromium.org (2014-07-30)

For the DOS part, heavy_file_io.html causes file descriptor outage in the browser process.
So, the browser process can't make shared memory anymore when it's under attacked, and anything doesn't go well.

### cl...@chromium.org (2014-08-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-05)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6604830963400704

Fuzzer: Therealholden_worker
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x6120001c7018
Crash State:
  - crash stack -
  content::EmbeddedSharedWorkerStub::OnMessageReceived
  content::MessageRouter::RouteMessage
  - free stack -
  content::EmbeddedSharedWorkerStub::OnMessageReceived
  content::MessageRouter::RouteMessage
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95EXXo7Hr3sVhYC6xObWRFNUMdpEAwVktEGOkoCcInhh8_cKRRO9vf5ve6RqxG5gmmRiptDxSjqKkitolptNoO_Y5jz-KB6KdjchHez21z_ZBRMhHA76BzzFj23JytXREKjoARsqKP9_MOrq1O9YlCiaKs9jA


Additional requirements: Requires Gestures

Filer: inferno

### in...@chromium.org (2014-08-05)

Looks like revert worked. No more stacks anymore.

### cl...@chromium.org (2014-08-09)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ho...@chromium.org (2014-08-12)

According to the crash report, this crash has happened using 
- Chromium: r285878
- Blink: r178998

But kouhei@'s patch mentioned in #1 is r179011 in Blink side.
And it was reverted in r179088.

So I think this patch is not related to this crash.

inferno@
Is my understanding correct?

### in...@chromium.org (2014-08-12)

Yes your understanding is right, my bad, please feel free to revert. I think this is some other worker related change that fixed it.

### in...@chromium.org (2014-08-14)

Looks like we are seeing the crash again, and now we see http://src.chromium.org/viewvc/blink?view=rev&revision=180013 in the regression range. Testcase coming and reopening bug for your analysis.

### cl...@chromium.org (2014-08-14)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6045409706246144

Fuzzer: Inferno_layout_test_unmodified
Job Type: Windows_syzyasan_content_shell

Crash Type: Use-after-free READ 4
Crash Address: 0x055eb8a3
Crash State:
  - crash stack -
  blink::WebSharedWorkerImpl::stopWorkerThread
  content::EmbeddedSharedWorkerStub::OnMessageReceived
  - free stack -
  operator delete
  blink::WebSharedWorkerImpl::stopWorkerThread
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=windows_syzyasan_content_shell&range=288872:289059

Minimized Testcase (0.15 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv97VaxLwj2-5btTqEksbv8G5K8iGvfzyLu2PhLCPRvLCqB6yhri1yMqItVj-bMG5SLHFUXoiMOEaa2ONpJoVTMb84OjIyp93i45plRn6WSOj0wWK7Yp94dxZBFkLo1yZx6iqWhch1heoUiYC8RNIWN9oubDQSQ
<script>
function log(message)
{
}

try {
} catch (error) {
}

try {
    new SharedWorker("http://example.com/worker.js");
} catch (error) {
}

</script>


Filer: inferno

### ho...@chromium.org (2014-08-14)

r180013 is reverted in r180031.
And fixed version landed in r180239.
https://codereview.chromium.org/451603002/

### cl...@chromium.org (2014-08-14)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-09-23)

Blink branched at 180365 for M38, so this should already be in M38.

### ti...@chromium.org (2014-10-07)

$1500 for this bug. ($1000 for the report, $500 bonus from ClusterFuzz). 

Reward Panel notes: Does not seem to have control between use and free, too many common stack frames, likely very hard to do anything other than crash with this. 

### cl...@chromium.org (2014-11-20)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2014-12-08)

Payment in progress

### ti...@google.com (2014-12-09)

[Empty comment from Monorail migration]

### ti...@google.com (2014-12-22)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/398198?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080120)*
