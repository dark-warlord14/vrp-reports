# Heap-use-after-free in webkit_glue::WebURLLoaderImpl::Context::OnReceivedResponse

| Field | Value |
|-------|-------|
| **Issue ID** | [40077563](https://issues.chromium.org/issues/40077563) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | ga...@chromium.org |
| **Created** | 2013-05-15 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

use-after-free with showModalDialog

**VERSION**  

Chrome Version: stable + dev  

Operating System: ubuntu 64bit

**REPRODUCTION CASE**

<script type="text/javascript" src="x"></script>
<script type="text/javascript">
showModalDialog("javascript:close()")
</script>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab+asan  

Crash State:

==9300==ERROR: AddressSanitizer: heap-use-after-free on address 0x60700001b8d0 at pc 0x55555ef0fc49 bp 0x7fffffff96f0 sp 0x7fffffff96e8  

READ of size 8 at 0x60700001b8d0 thread T0 (asan-release)  

#0 0x55555ef0fc48 in OnReceivedResponse /b/build/slave/ASAN\_Release/build/src/out/Release/../../webkit/glue/weburlloader\_impl.cc:658  

#1 0x55555b96f351 in OnReceivedResponse /b/build/slave/ASAN\_Release/build/src/out/Release/../../content/common/resource\_dispatcher.cc:349  

#2 0x55555b96e9e5 in DispatchToMethod<content::ResourceDispatcher, void (content::ResourceDispatcher::\*)(int, const content::ResourceResponseHead &), int, content::ResourceResponseHead> /b/build/slave/ASAN\_Release/build/src/out/Release/../../base/tuple.h:553

0x60700001b8d0 is located 32 bytes inside of 80-byte region [0x60700001b8b0,0x60700001b900)  

freed by thread T0 (asan-release) here:  

#0 0x555556a13d52 in operator delete(void\*) ??:0  

#1 0x55555ef10f37 in Release /b/build/slave/ASAN\_Release/build/src/out/Release/../../base/memory/ref\_counted.h:92  

#2 0x55555f6f96ba in deleteOwnedPtr[WebKit::WebURLLoader](javascript:void(0);) /b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/wtf/OwnPtrCommon.h:47  

#3 0x55555f6f88c6 in deleteOwnedPtr[WebCore::ResourceHandleInternal](javascript:void(0);) /b/build/slave/ASAN\_Release/build/src/out/Release/../../third\_party/WebKit/Source/wtf/OwnPtrCommon.h:47

## Attachments

- [stable-bug.txt](attachments/stable-bug.txt) (text/plain; charset=us-ascii, 7.3 KB)
- [bug.html](attachments/bug.html) (text/plain; charset=us-ascii, 139 B)
- [bug.txt](attachments/bug.txt) (text/plain; charset=us-ascii, 12.1 KB)

## Timeline

### in...@chromium.org (2013-05-15)

\please use llvm-symbolizer in the future to get namespaces in function names.

### in...@chromium.org (2013-05-15)

Can you reproduce this on trunk ? I can't. is there some other magic required ??

### mi...@gmail.com (2013-05-16)

<script type="text/javascript" src="http://google.com/x-y-z"></script>
<script type="text/javascript">
  showModalDialog("javascript:close()")
</script>

oops, I forgot, the first script must be on http schema, with the above it reproduces from file:// schema aswell.

### in...@chromium.org (2013-05-16)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=184660605

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60d0000267b0
Crash State:
  - crash stack -
  webkit_glue::WebURLLoaderImpl::Context::OnReceivedResponse
  content::ResourceDispatcher::OnReceivedResponse
  - free stack -
  webkit_glue::WebURLLoaderImpl::~WebURLLoaderImpl
  WebCore::ResourceHandleInternal::~ResourceHandleInternal
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=141190:141193

Minimized Testcase (0.10 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv97ZHOVCW07XmtDCvQ7_QXqNbMrJev1pQF5mnI5wav-KRa3QI5RpYttjM-LeqMv8zo1ZA_SwMjSx7nBtoJgsMFD7GZa8sRFtbfrsmefusvP-fhtaSlr4t40qc60XKNRGbSiKYrOJcOCoOFI4hA6VmGSsALHJtQ
<script src="http://google.com/x-y-z"></script>

<script>
  showModalDialog("javascript:close()")
</script>

### in...@chromium.org (2013-05-16)

The stack is exactly similar to http://trac.webkit.org/changeset/139551 which we fixed sometime back. Any idea what we missed there ?

### ja...@chromium.org (2013-05-16)

The path to triggering the deletion of the WebURLLoader is different. I think what is happening here is that, from within a nested runloop, we receive the IPC that the load is complete, which will synchronously release the WebURLLoader.

Gavin, do you have thoughts on what the proper fix is? In blink, tradition would demand a RefPtr protector in cancel(), but that doesn't seem to be how things are usually done in the chromium repo.

### in...@chromium.org (2013-05-17)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-05-20)

Talked to Gavin, he will take a look. Thanks Gavin.

### in...@chromium.org (2013-05-20)

[Empty comment from Monorail migration]

### ga...@chromium.org (2013-05-22)

Gah.

There's even a test for this: https://codereview.chromium.org/11778083/

But it was reverted in r176897 (same day it landed), probably due to this bug.

### in...@chromium.org (2013-05-22)

Good that you won't need to put more time into it since the unit test is there. Sad part is we should not reverting tests :(

### jl...@chromium.org (2013-05-24)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-05-28)

https://codereview.chromium.org/15738007/

friendly ping :)

### ga...@chromium.org (2013-05-28)

Yes, I'm advancing the CL per Darin's suggestion. I thought from his comments that he was going to do research, but it turns out he wanted me to do that. So I'll offer up an alternative shortly.

### in...@chromium.org (2013-05-29)

https://src.chromium.org/viewvc/chrome?view=rev&revision=202821

### in...@chromium.org (2013-06-04)

Patch was relanded as

https://src.chromium.org/viewvc/blink?view=rev&revision=151609
https://src.chromium.org/viewvc/chrome?view=rev&revision=203935

r202821 was reverted previously.

### cl...@chromium.org (2013-06-05)

ClusterFuzz has detected this issue as fixed in range 203930:203936.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=184660605

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60d0000267b0
Crash State:
  - crash stack -
  webkit_glue::WebURLLoaderImpl::Context::OnReceivedResponse
  content::ResourceDispatcher::OnReceivedResponse
  - free stack -
  webkit_glue::WebURLLoaderImpl::~WebURLLoaderImpl
  WebCore::ResourceHandleInternal::~ResourceHandleInternal
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=141190:141193
Fixed: https://cluster-fuzz.appspot.com/revisions?range=203930:203936

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97ZHOVCW07XmtDCvQ7_QXqNbMrJev1pQF5mnI5wav-KRa3QI5RpYttjM-LeqMv8zo1ZA_SwMjSx7nBtoJgsMFD7GZa8sRFtbfrsmefusvP-fhtaSlr4t40qc60XKNRGbSiKYrOJcOCoOFI4hA6VmGSsALHJtQ

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2013-06-11)

M28: Blink r152173 and Chromium r205381

### pa...@chromium.org (2013-06-27)

$1000 for this one!

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties.
*********************************

### sc...@gmail.com (2013-07-03)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-08-20)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/241139?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077563)*
